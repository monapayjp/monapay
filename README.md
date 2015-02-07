# Monapay
Monapay is a micro webservice providing a payment page to sell your products. Using this code, you can easily launch the website providing a payment page with regard to cryptocurrencies (e.g. Monacoin).

# Setup
Monapay uses Python 2.7 and Django 1.6. If you want to know the details, please see ``requirements.txt`` in the root directory. Monapay works well if your environment satisfies the list of ``requirements.txt`` (Note that this list contains several unused libraries). If you want to launch the monapay in your local environment, please follow the steps below:

1. Make a new environment and install additional libraries using ``pip install -r requirements.txt`` command.
2. Launch ``monacoind`` and set the username and its password appropriately.
3. Set ``MONACOIND_ADMIN_USER``, ``MONACOIND_ADMIN_PASSWORD``, ``MONACOIND_HOST``, ``MONACOIND_PORT`` variables in ``/payment/settings.py`` to appropriate values.
4. Launch a local webserver using ``python manage.py runserver``.

# Security
I DO NOT guarantee the security of Monapay. Please carefully check the whole code and confirm whether it does not contain any potential security vulnerabilities. I consider that it is hard for attackers to attack Monapay because it immediately send most of the money to the customers, however, you need to carefully design the entire configuration minimizing the damage by attackers.

# License
Monapay is licensed under 3-clause BSD License.
