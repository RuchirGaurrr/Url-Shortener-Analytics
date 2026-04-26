from user_agents import parse
import requests
from .models import Click

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def get_country_from_ip(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
        data = response.json()
        if data.get('status') == 'success':
            return data.get('country', 'Unknown')
    except Exception:
        pass
    return 'Unknown'

def log_click(request, short_url):
    try:
        ip = get_client_ip(request)
        country = get_country_from_ip(ip)
        ua_string = request.META.get('HTTP_USER_AGENT','')
        user_agent = parse(ua_string)

        device = 'mobile' if user_agent.is_mobile else 'tablet' if user_agent.is_tablet else 'desktop'
        browser = user_agent.browser.family


        Click.objects.create(
            short_url = short_url,
            ip_address = ip,
            device = device,
            browser = browser,
            country = country
        )

        short_url.clickcount += 1
        short_url.save(update_fields=['clickcount'])
    except Exception as e:
         print(f"Error logging click: {e}")