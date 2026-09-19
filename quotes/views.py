#views.py
#Sion Zhan (sszhan24@bu.edu), 9/10/26
#Description: Views for the quotes app. Handles random single-quote page,
# show-all page, and about page.

import random
from django.shortcuts import render

quotes = [
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "You have enemies? Good. That means you've stood up for something, sometime in your life.",
    "Men occasionally stumble over the truth, but most of them pick themselves up and hurry off as if nothing had happened.",
    "If you are going through hell, keep going.",
    "Success is stumbling from failure to failure with no loss of enthusiasm.",
    "Tact is the ability to tell someone to go to hell in such a way that they look forward to the trip.",
    "Never, never, never give in!",
    "It is not enough that we do our best; sometimes we must do what is required.",
    "Kites rise highest against the wind, not with it.",
    "Continuous effort - not strength or intelligence - is the key to unlocking our potential.",
]

images = [
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/02/Sir_Winston_Churchill_-_19086236948_%28restored%29.jpg/500px-Sir_Winston_Churchill_-_19086236948_%28restored%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7c/Winston-Churchill1.jpg/330px-Winston-Churchill1.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5d/Winston_Churchill_by_William_Orpen%2C_1916%2C.jpg/330px-Winston_Churchill_by_William_Orpen%2C_1916%2C.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f9/Sir_Winston_Churchill_%28statesman%29_Detail.jpg/330px-Sir_Winston_Churchill_%28statesman%29_Detail.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/35/Churchill_portrait_NYP_45063.jpg/330px-Churchill_portrait_NYP_45063.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d0/Winston_Churchill_cph.3b12010.jpg/330px-Winston_Churchill_cph.3b12010.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail:,",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9c/Sir_Winston_S_Churchill.jpg/330px-Sir_Winston_S_Churchill.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/97/Churchill_HU_90973.jpg/330px-Churchill_HU_90973.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c5/Churchil_at_the_Tehran_Conference_1943.jpg/250px-Churchil_at_the_Tehran_Conference_1943.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/cd/Churchill_V_sign_HU_55521.jpg/250px-Churchill_V_sign_HU_55521.jpg?utm_source=commons.wikimedia.org&utm_campaign=parser&utm_content=thumbnail"
]

def quote(request):
    '''Display randomly selected quote and image pair.'''

    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    '''Display all quotes and images (one row per quote).'''

    context = {
        'quotes': quotes,
        'images': images,
    }

    return render(request, 'quotes/show_all.html', context)

def about(request):
    '''Display biographical information about Winston Churchill,
    along with a brief note about the author of the app.'''

    context = {
        'person_name': 'Winston Churchill',
        'birth_year': '1874',
        'death_year': '1965',
        'birthplace': 'Blenheim Palace Woodstock',
        'bio': (
            "Sir Winston Churchill was a British statesman, solider, "
            "and writer who served as Prime Minister of the UK twicce and led "
            "the nation to victory during WWII. Born into an aristocratic British-"
            "American family, he graudated from the Royal Military College, serving as "
            "a solider and journalist in Cuba, India, and South Africa. Elected as a "
            "Conservative Member of Parliament in 1900. He recieved a knighthood and "
            "the Nobel Prize in Literature in 1953 for his historical writings."
        ),
        'author_name': 'Sion Zhan',
        'author_bio': (
            "This app was built by me, a student at BU, as part of the CS412 Web"
            "Application Development course."
        ),
        'creation_date': 'Fall 2026',
    }
    return render(request, 'quotes/about.html', context)




