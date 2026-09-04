from django.shortcuts import render


def bienvenida(request):
	return render(request, 'transport_app/bienvenida.html')


def error_404(request, exception):
	return render(request, 'transport_app/404.html', status=404)
