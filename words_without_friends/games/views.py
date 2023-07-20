from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Games
import random, string

@login_required
def game(request):
  letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
  if request.method == 'POST':
    words = request.POST.get('words')
    words_list = words.split(",")
    game = Game.objects.create(user=request.user, letters=letters, words=words, score=len(words_list))
    return render(request, 'score.html', {'game': game})
  return render(request, 'game.html', {'letters': letters})

@csrf_exempt
def check_word(request):
  if request.is_ajax():
    word = request.GET.get('word', None)
    letters = request.GET.get('letters', None)
    is_valid = all(word.count(letter) <= letters.count(letter) for letter in set(word))
    
    data = {
      'is_valid': is_valid
    }
    return JsonResponse(data)
