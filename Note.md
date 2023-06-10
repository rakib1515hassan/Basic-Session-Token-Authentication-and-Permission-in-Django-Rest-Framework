# NOTE Token Genarate------------------

    1) Add this in your setting.py file. After past this mast be migrations migrate commend run.
        INSTALLED_APPS = [
            'rest_framework.authtoken'
        ]
    2) Token Genaret:
         a) Genaret token by admin pannel ( এই ক্ষেত্রে আপনাকে মেনুয়ালি token create করতে হবে )
         b) DRF commend , go powershell = python manage.py drf_create_token you_username এটি দিলে ঐ user এর নামে token table এ
            একটি টোকেন create হয়ে যাবে।
         c) By exposing an API endpoint:
                (i) import this in your urls.py-----
                    from rest_framework.authtoken.views import obtain_auth_token

                (ii) Go to Terminal in Command Prompt run (একবার ই run কোরতে হবে then save it in env) = pip install httpie

                (iii) URL Hit on Command Prompt and token autometically given and save it on authtoken_token Table/Model
                    # To hit this url (http POST http://127.0.0.1:8000/authtoken_genarate/ username="your_username" password="your_password")
                    path('authtoken_genarate/', obtain_auth_token)
                    
            *** (iv) যদি view.py এর কোন Class or Function থেকে Custom Token create কোরতে চাই তবে, প্রথমে আমাদেরকে একটি CustomAuthToken class নিতে 
                     হবে। এক্ষেত্রে আমরা এটির জন্যে আলাদা auth.py নিয়ে এর ভেতর আথবা direct view.py এর ভেতর CustomAuthToken class নিব। যা আমরা
                     এই Project এ Accounts app এর ভেতর করেছি।
                     এর পর আমাদের Accounts urls.py এর ভেতর path('authtoken_genarate/', obtain_auth_token), এই URL এর পরিবর্তে 
                     path('custom_authtoken_genarate/', CustomAuthToken.as_view()), এটি ব্যবহার কোরব Token Genarete করার জন্যে। এখানে মনে 
                     রাখতে হবে যে , যে class or function থেকে CustomAuthToken কে Call করি না কেন তা অবশ্যই POST method এর ভেতর থেকে হতে হবে।
        
         d) Using Signals: এই ক্ষেত্রে আমরা যে code টি লিখতে হবে তা Accounts app এর Models এর ভেতর create_auth_token function এ লেখা হয়েছে। 
         এতে যখনি user create হবে, তখনি Tokene Auto Create হয়ে তা Database এ auto save হয়ে যাবে।


# NOTE API Testing------------------( HTTPie )

    Definition: HTTPie (pronounced aitch-tee-pie) is a command line HTTP clint. Its goal is to make CLI interaction with web services ad 
                human-friendly as possible. It provides a simple http command that allows for sending arbitrary HTTP requests using a
                simple and natural syntax, and displays colorized output. HTTP servere.

                Basic Syntex:- http[flags][METHOD]URL[ITEM[ITEM]]
                Example:- 
                    (i) GET Request = http http://127.0.0.1:8000/your_url_on_urls_py/

                        If Token = http http://127.0.0.1:8000/your_url_on_urls_py/'Authorization:Token give_here_your_token'

                    (ii) POST Request = http -f POST http://127.0.0.1:8000/your_url_on_urls_py/ name=abc roll=000 city=Dhaka 'Authorization:Token    give_here_your_token'

                    (iii) DELETE Request = http DELETE http://127.0.0.1:8000/your_url_on_urls_py/4/'Authorization:Token give_here_your_token'

    Installation: pip install httpie এই commend টিকে Command Prompt run করতে হবে। (একবার ই run কোরতে হবে then save it on your virtual env)




