import time
from django.shortcuts import render


class MassCrashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = []

    def __call__(self, request):
        # проверяем, что запрос POST и идет на страницу user
        if request.method == 'POST' and request.path == '/user/':
            # получаем данные из запроса
            email = request.POST.get('email')
            location = request.POST.get('location')
            # добавляем запрос в список
            self.requests.append({'email': email, 'location': location, 'timestamp': time.time()})
            # удаляем из списка запросы, которые были более 10 секунд назад
            self.requests = [r for r in self.requests if time.time() - r['timestamp'] <= 10]
            # считаем количество запросов с расстоянием в 10 метров
            count = len([r for r in self.requests if r['location'] == location])
            # если количество запросов больше 3, возвращаем страницу с сообщением о массовой аварии
            if count > 3:
                return render(request, 'mass_crash.html')
        # возвращаем результат выполнения следующего middleware или view
        response = self.get_response(request)
        return response
