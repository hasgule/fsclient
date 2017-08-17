from .models import Venue, VenueSearch, Chat, Display, UserProfile
from .forms import SignUpForm, ContactForm
from django.contrib import messages
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
from itertools import chain

def venue_history_find(request):
    if request.user.is_authenticated():
        venue_search_history = VenueSearch.objects.filter(owner=request.user).values('query', 'near')
        venue_search_list = list(venue_search_history)
        query_list = list()
        near_list = list()
        for venue in venue_search_list:
            query_list.append(venue["query"])
            near_list.append(venue["near"])
        my_list = [query_list] + [near_list]
        return JsonResponse(my_list, safe=False)
    return None


def my_profile(request):
    unviewed_chat_number = control_messages(request)

    if request.FILES.get('image'):
        new_image = request.FILES.get('image')
        user = request.user
        my_user = UserProfile.objects.filter(user=user).first()
        my_user.image = new_image
        my_user.save()
    if request.GET.get('name'):
        username = request.GET.get('name')
        my_user = UserProfile.objects.filter(username=username).first()
        if request.user == my_user:
            pass
        else:
            Display.objects.create(displayed_by=request.user, displayed=my_user.user)
    else:
        my_user = request.user
    active_user = request.user
    return render(request, 'wheretoeat/my_profile.html', {'desired_user': my_user, 'active_user': active_user,
                                                          'unviewed_chat_number': unviewed_chat_number})


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
        username = request.POST.get('user__name')
        new_user = User.objects.get(username=username)
        new_password = request.POST.get('newpassword1')
        new_user.set_password(new_password)
        new_user.save()
        user = authenticate(username=username, password=new_password)
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
            if User.objects.filter(email=email_sending).exists():
                subject = 'Password Recovery Email'
                text_content = 'This is an important message.'
                email_html = get_template('registration/reset_email.html')
                user_name = User.objects.filter(email=email_sending).first()
                d = Context({'username': user_name})
                html_content = email_html.render(d)
                message = EmailMultiAlternatives(subject, text_content, 'noreply@foursquareclient.com', [email_sending])
                message.attach_alternative(html_content, "text/html")
                message.send()
                return redirect('wheretoeat:password_reset_done')
            else:
                messages.warning(request, 'Enter a valid email address.')
                return render(request, "registration/password_reset_form.html", {'form': form})
        else:
            return render(request, "registration/password_reset_form.html", {'form': form})
    return render(request, "registration/password_reset_form.html", {'form': form})


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


def login_user(request):
    desired_searches = ()
    user_list = User.objects.filter()
    temporary_list = user_list[:3]
    desired_users = reversed(temporary_list)
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
                    unviewed_chat_number = control_messages(request)
                    my_searches = VenueSearch.objects.filter(owner=request.user)
                    desired_searches = list(islice(reversed(my_searches), 0, 5))
                    return render(request, 'wheretoeat/result.html', {'searches': desired_searches,
                                                                      'user_query': desired_users,
                                                                      'unviewed_chat_number': unviewed_chat_number})
                else:
                    messages.warning(request, 'Your username or password is wrong, please check again.')
                    return render(request, 'registration/login.html')
            else:
                messages.warning(request, 'Your username or password is wrong, please check again.')
                return render(request, 'registration/login.html')
        else:
            messages.warning(request, 'Your username or password is wrong, please check again.')
            return render(request, 'registration/login.html')


def log_out(request):
    auth_views.logout(request)
    return render(request, 'wheretoeat/result.html')


def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.username = form.cleaned_data.get('username')
            user.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            unviewed_chat_number = control_messages(request)
            return render(request, 'wheretoeat/result.html', {'unviewed_chat_number': unviewed_chat_number})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def signedup(request):
    unviewed_chat_number = control_messages(request)
    render(request, 'registration/signedup.html', {'unviewed_chat_number': unviewed_chat_number})


def sure_sign_out(request):
    return render(request, 'registration/sure_sign_out.html', {'YES': True})


def sign_out(request):
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
    if "errorType" in result["meta"]:
        return None
    elif (result["response"]["geocode"] is not None) and (result["response"]["venues"] is None):
        return None
    elif result["response"]["venues"]:
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
    url_cont = "?client_id=V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK&client_secret=L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF&v=20170423"
    search_url = url + venue_id + url_cont
    result = requests.get(search_url)
    json_result = result.json()
    venue_result = json_result["response"]["venue"]
    return venue_result


def get_prev(request):
    unviewed_chat_number = control_messages(request)

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
    return render(request, 'wheretoeat/venue_search.html', {'venues': paginated_venues,
                                                            'query': desired_query,
                                                            'near': desired_near,
                                                            'unviewed_chat_number': unviewed_chat_number})


def venue_list(request):
    unviewed_chat_number = control_messages(request)

    my__query = request.GET.get('my_query')
    my__near = request.GET.get('my_near')
    venues = get_venues(my__query, my__near)
    return render(request, 'wheretoeat/result.html', {'venues': venues, 'unviewed_chat_number': unviewed_chat_number})


def index(request):

    fifteen_user = get_fifteen_minutes_users()
    current_users = get_current_users()
    user_queries = User.objects.filter()
    desired_user_query = list(islice(reversed(user_queries), 0, 3))
    if request.GET.get('query_to_delete'):
        if request.GET.get('near_to_delete'):
            query_to_delete_ = request.GET.get('query_to_delete')
            near_to_delete_ = request.GET.get('near_to_delete')
            VenueSearch.objects.filter(query=query_to_delete_, near=near_to_delete_).delete()
    venues = None
    paginated_venues = None
    my_owner = None
    my_error = None
    my__query = None
    my__near = None
    page = request.GET.get('page', 1)
    if request.user.is_authenticated:
        my_owner = request.user
    if request.GET.get('my_query'):
        if request.GET.get('my_near'):
            my__query = request.GET.get('my_query')
            my__near = request.GET.get('my_near')
            venues = get_venues(my__query, my__near)
            if (venues == None) is False:
                if (request.GET.get('dont') == 'save') is False:
                    VenueSearch.objects.create(query=my__query, near=my__near, owner=my_owner)
                last_search_id = VenueSearch.objects.latest('id')
                for venue_result in venues:
                    phone = venue_result.get('phone_number', '')
                    Venue.objects.create(venue_id=venue_result['venue_id'], name=venue_result['name'],
                                         phone_number=phone, checkin_count=venue_result['checkin_count'],
                                         search_id=last_search_id)
            else:
                messages.warning(request, 'Please make a valid search!')
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
    if request.user.is_authenticated:
        unviewed_chat_number = control_messages(request)
        return render(request, 'wheretoeat/result.html', {'searches': desired_searches, 'venues': paginated_venues,
                                                      'current_fifteen_users': fifteen_user,
                                                      'user_query': desired_user_query, 'current_users': current_users,
                                                      'query': my__query, 'near': my__near, 'my_error': my_error,
                                                      'unviewed_chat_number': unviewed_chat_number})
    else:
        return render(request, 'wheretoeat/result.html', {'searches': desired_searches, 'venues': paginated_venues,
                                                          'current_fifteen_users': fifteen_user,
                                                          'user_query': desired_user_query,
                                                          'current_users': current_users,
                                                          'query': my__query, 'near': my__near, 'my_error': my_error})


def all_users(request):
    unviewed_chat_number = control_messages(request)

    my_list = UserProfile.objects.exclude(username=request.user.username)
    return render(request, 'wheretoeat/all_users.html', {'my_list': my_list,
                                                         'unviewed_chat_number': unviewed_chat_number})


def control_messages(request):
    unviewed_chat_number = 0
    list = Chat.objects.filter(to_user=request.user)
    for chat in list:
        if chat.is_viewed==False:
            unviewed_chat_number = unviewed_chat_number+1
    return unviewed_chat_number


def chatmessages(request):
    user = request.user
    from_messages = Chat.objects.filter(from_user=user)
    to_messages = Chat.objects.filter(to_user=user)
    result_list = sorted(chain(from_messages, to_messages), key=lambda instance: instance.created)
    if request.GET.get('message_to_delete'):
        message_to_delete = request.GET.get('message_to_delete')
        from_user = request.GET.get('from_user_to_delete')
        from_user_to_delete = UserProfile.objects.get(username=from_user)
        to_user = request.GET.get('to_user_to_delete')
        to_user_to_delete = UserProfile.objects.get(username=to_user)
        chat = Chat.objects.get(message=message_to_delete, from_user=from_user_to_delete.user,
                                to_user=to_user_to_delete.user)
        chat.delete()
    if request.GET.get('view'):
        user = request.GET.get('user')
        chats = Chat.objects.filter(to_user=request.user)
        for chat in chats:
            chat.is_viewed = True
            chat.save()
        unviewed_chat_number = control_messages(request)
        return render(request, 'wheretoeat/chatmessages.html', {'view': 'yes', 'user': user, 'chat_view': result_list,
                                                                'unviewed_chat_number': unviewed_chat_number})
    unviewed_chat_number = control_messages(request)
    user = request.user
    chats = Chat.objects.filter(to_user=user).order_by('-created')
    outbox = Chat.objects.filter(from_user=user).order_by('-created')

    return render(request, 'wheretoeat/chatmessages.html', {'chats': chats, 'outbox': outbox,
                                                            'unviewed_chat_number': unviewed_chat_number})


def message_sent(request):
    unviewed_chat_number = control_messages(request)

    message = request.POST.get('my_message')
    if request.POST.get('sent_to_user'):
        try:
            username = request.POST.get('sent_to_user')
            sent_to_user = UserProfile.objects.get(username=username)
            Chat.objects.create(message=message, from_user=request.user, to_user=sent_to_user.user)
            return render(request, 'wheretoeat/message_sent.html', {'unviewed_chat_number': unviewed_chat_number})
        except:
            messages.warning(request, 'Please enter a valid username')
            return render(request, 'wheretoeat/new_message_page.html', {'unviewed_chat_number': unviewed_chat_number})
    elif request.GET.get('sent_to_user'):
        username = request.GET.get('sent_to_user')
        sent_to_user = UserProfile.objects.get(username=username)
        Chat.objects.create(message=message, from_user=request.user, to_user=sent_to_user.user)
        return render(request, 'wheretoeat/message_sent.html', {'unviewed_chat_number': unviewed_chat_number})
    else:
        username = request.GET.get('user')
        to_user = UserProfile.objects.get(username=username)
        Chat.objects.create(message=message, from_user=request.user, to_user=to_user.user)
        return render(request, 'wheretoeat/message_sent.html', {'unviewed_chat_number': unviewed_chat_number})


def new_message_page(request):
    unviewed_chat_number = control_messages(request)

    if request.GET.get('my_to_user'):
        username = request.GET.get('my_to_user')
        if User.objects.get(username=username):
            to_user = User.objects.get(username=username)
            chat_list = Chat.objects.filter(from_user=to_user, to_user=request.user)
        else:
            to_user = None
            chat_list = None
        return render(request, 'wheretoeat/new_message_page.html', {'prev_chats': chat_list, 'chat_user': to_user,
                                                                    'unviewed_chat_number': unviewed_chat_number})
    else:
        return render(request, 'wheretoeat/new_message_page.html', {'unviewed_chat_number': unviewed_chat_number})


def who_displayed(request):
    unviewed_chat_number = control_messages(request)

    display_list = Display.objects.filter(displayed=request.user)
    my_list = reversed(display_list)
    return render(request, 'wheretoeat/whodisplayed.html', {'display_list': my_list,
                                                            'unviewed_chat_number': unviewed_chat_number})


def venue_details(request):
    venue_name = request.GET.get('venue_name')
    query = request.GET.get('query')
    near = request.GET.get('near')
    venues = get_venues(query, near)
    address = None
    name = None
    contact = None
    canonicalUrl = None
    checkin = None
    for venue in venues:
        if venue["name"] == venue_name:
            my_id = venue["venue_id"]
            information = get_venue_information(my_id)
            location = information.get("location", None)
            address = location.get("formattedAddress", None)
            name = information.get("name", None)
            if 'contact' in information:
                if 'phone' in information['contact']:
                    contact = information['contact']['phone']
            canonicalUrl = information.get("canonicalUrl", None)
            stats = information.get("stats", None)
            checkin = stats.get("checkinsCount", None)
    return render(request, 'wheretoeat/venue_details.html', {'location': address, 'name': name, 'contact': contact,
                                                             'canonicalUrl': canonicalUrl, 'stats': checkin})

