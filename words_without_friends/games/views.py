from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Game
import random, string
from .models import User
from django.shortcuts import render, redirect
from .forms import RegistrationForm
# from django.contrib.auth.models import User

@login_required
def game(request, id):
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        words = request.POST.get('words')
        words_list = words.split(",")
        score = len(words_list)
        letters = request.session.get('letters', None) # use session to get letters
        game = Game.objects.create(user=user, letters=letters, words=words, score=score)
        return render(request, 'score.html', {'game': game})
    else:
        letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        request.session['letters'] = letters # store letters in session
        return render(request, 'game.html', {'letters': letters})
    
@csrf_exempt
def check_word(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        word = request.GET.get('word', None)
        letters = request.session.get('letters', None)
        words_used = request.session.get('words_used', [])
        with open('static/dictionary.txt', 'r') as file:
          valid_words = file.read().splitlines()
        is_valid = word not in words_used and word in valid_words and all(word.count(letter) <= letters.count(letter) for letter in set(word)) 
        data = {
            'is_valid': is_valid
        }
        if is_valid:
          words_used.append(word)
          request.session['words_used'] = words_used
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "This is not an AJAX request."})

# def check_word(request):
#     if request.is_ajax():
#         word = request.GET.get('word', None)
#         letters = request.GET.get('letters', None)

#         # Assuming 'wordlist.txt' is your file containing a list of valid words


#         # Check if the word exists in the valid words list
#         is_valid = word in valid_words and all(word.count(letter) <= letters.count(letter) for letter in set(word))

#         data = {
#             'is_valid': is_valid
#         }
#         return JsonResponse(data)
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request, id):
  try:
    user = User.objects.get(pk=id)
  except User.DoesNotExist:
    return render(request,'404.html', status=404)
  if request.method == 'GET':
    context = {'user': user}
    return render(request, 'profile.html', context)