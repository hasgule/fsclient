from django.utils.translation import get_language, activate
from .models import Venue,VenueSearch, Chat, Display, UserProfile
from .forms import SignUpForm, ContactForm, ProfileForm
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from itertools import islice
import datetime
import requests
from django.http import JsonResponse

def venue_history_find(request):
    if request.user.is_authenticated():
        venuesearch_history = VenueSearch.objects.filter(owner=request.user).values('query', 'near')
        venuesearch_list = list(venuesearch_history)
        querylist = list()
        nearlist = list()
        for venue in venuesearch_list:
            querylist.append(venue["query"])
            nearlist.append(venue["near"])
        mylist = [querylist] + [nearlist]
        return JsonResponse(mylist, safe=False)
    return None

def my_profile(request):
    if request.FILES.get('image'):
        new_image = request.FILES.get('image')
        user = request.user
        my_user = UserProfile.objects.filter(user=user).first()
        my_user.image = new_image
        my_user.save()
    if request.GET.get('name'):
        user__name = request.GET.get('name')
        my__user = UserProfile.objects.filter(username=user__name)
        my_user = my__user.first()
        if request.user == my_user:
            pass
        else:
            display_object = Display.objects.create(displayed_by=request.user, displayed=my_user.user)
    else:
        my_user = request.user
    active_user = request.user
    return render(request, 'wheretoeat/my_profile.html', {'desired_user': my_user, 'active_user': active_user})


def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now(), )
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=user_id_list)


def get_fifteen_minutes_users():
    now_minus_15 = datetime.datetime.now() - datetime.timedelta(minutes=15)
    user_list = User.objects.filter(last_login__gte=now_minus_15)
    return user_list

def new_password_form(request):
    return render(request, 'registration/new_password_form.html')

def successful_change(request):
    if request.POST.get('newpassword1') == request.POST.get('newpassword2'):
        user_name = request.POST.get('user__name')
        new_user = User.objects.get(username=user_name)
        newpassword = request.POST.get('newpassword1')
        new_user.set_password(newpassword)
        new_user.save()
        user = authenticate(username=user_name, password=newpassword)
        login(request, user)
        return render(request, 'registration/successful_change.html', {'different_pw': False})
    else:
        return render(request, 'registration/new_password_form.html', {'different_pw': True})

def password_reset(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email_sending = request.POST.get('email_sending')
            if User.objects.filter(email = email_sending).exists():
                subject = 'Password Recovery Email'
                text_content = 'This is an important message.'
                email_html = get_template('registration/reset_email.html')
                user_name = User.objects.filter(email=email_sending).first()
                print(user_name)
                d = Context({'username': user_name})
                html_content = email_html.render(d)
                msg = EmailMultiAlternatives(subject, text_content, 'noreply@foursquareclient.com', [email_sending])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('wheretoeat:password_reset_done')
    return render(request, "registration/password_reset_form.html", {'form': form})


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def login_user(request):
    user_queries = User.objects.filter()
    temporary_queries = user_queries[:3]
    desired_user_query = reversed(temporary_queries)
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.user.is_authenticated:
                    my_searches = VenueSearch.objects.filter(owner=request.user)
                    desired_searches = list(islice(reversed(my_searches), 0, 5))
                return render(request, 'wheretoeat/result.html', {'searches': desired_searches, 'user_query':desired_user_query})
        else:
            return render(request, 'wheretoeat/result.html')

def log_out(request):
    auth_views.logout(request)
    return render(request, 'wheretoeat/result.html')


def SignUp(request):
    if request.method == 'POST':
         form = SignUpForm(request.POST)
         if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.email = form.cleaned_data.get('email')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.username = form.cleaned_data.get('username')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('wheretoeat:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def signedup(request):
    render(request, 'registration/signedup.html')

def sign_out(request):
    print(request.POST.get("YES"))
    if request.POST.get('YES', False):
        my_user = UserProfile.objects.get(username=request.user.username)
        my_user.delete()
        User.objects.get(username=request.user.username).delete()
        return render(request, 'registration/sign_out.html', {'YES': True})
    else:
        return render(request, 'registration/sign_out.html')

def get_venues(query, near):
    url = "https://api.foursquare.com/v2/venues/search?client_id=V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK&client_secret=L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF&v=20170423"
    params = {'near': near, 'query': query}
    r = requests.get(url, params=params)
    result = r.json()
    if result["response"]:
        if result["response"]["venues"]:
            res = result["response"]["venues"]
            l = list()
            for r in res:
                obj = dict()
                obj['venue_id'] = r["id"]
                obj['name'] = r["name"]
                obj['phone_number'] = None
                if r["contact"]:
                    obj['phone_number'] = r["contact"].get("phone", '')
                else:
                    obj['phone_number'] = ''
                    obj['checkin_count'] = r["stats"]["checkinsCount"]
                    l.append(obj)
                return l


def get_venue_information(venue_id):
    url = "https://api.foursquare.com/v2/venues/"
    id = venue_id
    url_cont = "?client_id=V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK&client_secret=L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF&v=20170423"
    search_url = url + id + url_cont
    result = requests.get(search_url)
    json_result = result.json()
    venue_result = json_result["response"]["venue"]
    return venue_result

def get_prev(request):
    desired_query = request.GET.get('query')
    desired_near = request.GET.get('near')
    desired_venues = list()
    for venue in get_venues(desired_query, desired_near):
        desired_venues.append(venue)
    page = request.GET.get('page', 1)
    paginator = Paginator(desired_venues, 10)
    try:
        paginated_venues = paginator.page(page)
    except PageNotAnInteger:
        paginated_venues = paginator.page(1)
    except EmptyPage:
        paginated_venues = paginator.page(paginator.num_pages)
    return render(request, 'wheretoeat/venue_search.html',
                  {'venues': paginated_venues, 'query': desired_query, 'near': desired_near})


def venue_list(request):
    my__query = request.GET.get('my_query')
    my__near = request.GET.get('my_near')
    venues = get_venues(my__query, my__near)
    return render(request, 'wheretoeat/result.html', {'venues': venues})


def index(request):
    current_language = get_language()
    print(current_language)
    fifteen_user = get_fifteen_minutes_users()
    current_users = get_current_users()
    user_queries = User.objects.filter()
    desired_user_query = list(islice(reversed(user_queries), 0, 3))

    if (request.GET.get('query_to_delete')):
        if(request.GET.get('near_to_delete')):
            query_to_delete_ = request.GET.get('query_to_delete')
            near_to_delete_ = request.GET.get('near_to_delete')
            VenueSearch.objects.filter(query=query_to_delete_,near= near_to_delete_).delete()
    venues = None
    paginated_venues = None
    my_owner = None
    my_error = None
    my__query = None
    my__near = None
    page = request.GET.get('page', 1)
    if request.user.is_authenticated:
        my_owner = request.user
    if (request.GET.get('my_query')):
        if(request.GET.get('my_near')):
            my__query = request.GET.get('my_query')
            my__near = request.GET.get('my_near')
            if my__query and my__near:
                if request.GET.get('page') is None and get_venues(my__query, my__near) is not None:
                    query = VenueSearch.objects.create(query=my__query, near=my__near, owner=my_owner)
                last_search_id = VenueSearch.objects.latest('id')
                if get_venues(my__query, my__near) is not None:
                    venues = get_venues(my__query, my__near)
                    if request.GET.get('page') is None:
                        for venue_result in venues:
                            myPhone = venue_result.get('phone_number', '')
                            venue_query = Venue.objects.create(venue_id = venue_result['venue_id'],name=venue_result['name'], phone_number=myPhone,
                                                               checkin_count=venue_result['checkin_count'], search_id=last_search_id)
                            venue_query.save()

    if venues:
        paginator = Paginator(venues, 10)
        try:
            paginated_venues = paginator.page(page)
        except PageNotAnInteger:
            paginated_venues = paginator.page(1)
        except EmptyPage:
            paginated_venues = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        my_searches = VenueSearch.objects.filter(owner=my_owner)
        desired_searches = list(islice(reversed(my_searches), 0, 5))
    else:
        desired_searches = list()
    return render(request, 'wheretoeat/result.html', {'searches': desired_searches, 'venues': paginated_venues, 'current_fifteen_users': fifteen_user,'user_query': desired_user_query, 'current_users': current_users, 'query':my__query, 'near':my__near, 'my_error':my_error})

def all_users(request):
    my_list = UserProfile.objects.exclude(username=request.user.username)
    return render(request, 'wheretoeat/all_users.html', {'my_list':my_list})

def messages(request):
    chats = Chat.objects.filter(to_user=request.user).order_by('-created')
    return render(request, 'wheretoeat/messages.html', {'chats':chats})

def message_sent(request):
    my_to_user = request.POST.get('my_to_user')
    my_message = request.POST.get('my_message')
    new_chat = Chat.objects.create(message=my_message, from_user = request.user, to_user = my_to_user)
    return render(request, 'wheretoeat/message_sent.html')

def new_message_page(request):
    if request.GET.get('my_to_user'):
        my_to_user = request.GET.get('my_to_user')
        return render(request, 'wheretoeat/new_message_page.html', {'my_to_user':my_to_user})
    else:
        return render(request, 'wheretoeat/new_message_page.html')

def who_displayed(request):
    display_list = ()
    display_list = Display.objects.filter(displayed=request.user)
    list = reversed(display_list)
    return render(request, 'wheretoeat/whodisplayed.html', {'display_list': list})

def sure_sign_out(request):
    return render(request, 'registration/sure_sign_out.html', {'YES': True})

def venue_details(request):
    venue_name = request.GET.get('venue_name')
    query = request.GET.get('query')
    near = request.GET.get('near')
    venues = get_venues(query,near)
    address = None
    name = None
    contact = None
    canonicalUrl = None
    checkin = None
    for venue in venues:
        if(venue["name"]==venue_name):
            my_id = venue["venue_id"]
            information = get_venue_information(my_id)
            location = information.get("location", None)
            address = location.get("formattedAddress", None)
            name = information.get("name", None)
            if 'contact' in information:
                if 'phone' in information['contact']:
                    contact = information['contact']['phone']
            canonicalUrl = information.get("canonicalUrl",None)
            stats = information.get("stats",None)
            checkin = stats.get("checkinsCount", None)
    return render(request, 'wheretoeat/venue_details.html', {'location': address, 'name': name, 'contact': contact , 'canonicalUrl': canonicalUrl, 'stats': checkin})