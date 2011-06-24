##############################################
 nagifo - Send nagios alerts via notifo
##############################################

:Version: 0.2.0

Introduction
------------

Nagifo is a simple little package to send nagios alerts to your mobile phone
via `Notifo`_, and to allow you to acknowledge nagios alerts without having to
login to nagios.



Installation
------------

You can install nagifo off the cheeseshop using ``pip`` or ``easy_install``, or
you can install from source.

To install using ``easy_install``,::

    $ easy_install nagifo

To install using ``pip``,::

    $ pip install nagifo

If you've downloaded the source tarball off the cheeseshop, or cloned the
nagifo repository, you can install nagifo like so::

    $ python2 setup.py install


Configuration
-------------

Notifo
======

Any further configuration requires a `Notifo`_ account, so go sign up if you
haven't already (accounts are free). You will also require your Notifo API key.
You can find your personal API key on the `Notifo user settings`_ page.

Since the entire point of this (at least for me) is to get alerts on a mobile
phone, you'll probably also want to install the `Notifo`_ client on your phone.

Note, everybody in your organization who wants notifications via Notifo will
require their own `Notifo`_ account.


Nagios Configuration
====================

Setting up nagios to use nagifo to send notifications is as simple as I could
figure out how to make it. 

You will require a command definition, which is what actually runs the nagifo
command (make sure nagifo is in your $PATH!). These are commonly located in
``commands.cfg``. Here is the command definition to use::

    define command{
            command_name    notify-by-notifo
            command_line    nagifo \
              "$CONTACTADDRESS1$" "$CONTACTADDRESS2$" "$NOTIFICATIONTYPE$" "$HOSTNAME$" \
              "$SERVICESTATE$" "$SERVICEDESC$" "$SERVICEOUTPUT$ $LONGDATETIME$"
            }


To get Nagios to send you an alert over `Notifo`_, you need to tell Nagios to
run the ``notify-by-notifo`` command when sending an alert to you. This is done
by adding the following line to your contact definition::

        service_notification_commands   +notify-by-notifo

And since the nagifo script requires the username and API key of the user that
it will be alerting, these are also required in the contact definition. As I
have no idea if Nagios supports arbitrary fields in a contact definition,
I've used the ``address1`` field for the notifo username, and the ``address2``
field for the notifo API key.::

        address1                        <notifo-username>
        address2                        <notifo-API-key>

Here's what an example of what a complete contact definition looks like::

    define contact{
            contact_name                    jdoe
            use                             generic-contact
            alias                           John Doe
            email                           jdoe@company.com
            address1                        jdoe
            address2                        lkjsdf908234234kjndflkjsdf2342345439sdfsdf3
            service_notification_commands   +notify-by-notifo
            }


Acknowledging from Notifo
=========================

Included with this package is a little webapp that will allow you to
acknowledge alerts from your phone, without needing to log in to nagios.
Configuration of this webapp is admittedly more involved.

For the sake of brevity, I'm going to assume you're using apache2 to serve
nagios, and have mod_wsgi installed and already loaded. That said, the quickest
way of getting the webapp working is to add the following to the apache2
configuration file::

    WSGIScriptAliasMatch /nagifo /var/www/nagifo.wsgi

The contents of ``/var/www/nagifo.wsgi`` are simply::

    from nagifo.nagacknowledge import app as application

If your setup differs from my assumptions, or more details are required, take a
look at the `Flask deployment guide`_.

The final thing required is the nagifo configuration file. The nagifo config
file is located at ``/etc/nagifo.conf``, and looks like::

    [default]
    nagios_cmdfile = /usr/local/nagios/var/rw/nagios.cmd
    secret_key = some_long_random_string22
    external_url = nottaken.net:4444/nagifo

You'll need to find where your nagios install puts its nagios.cmd file, and
set ``nagios_cmdfile`` to the path of that file.

The ``secret_key`` should be some long random string. The purpose of the string
is to act like a password and prevent random strangers from acknowledging your
alerts by simply guessing at the url.

The ``external_url`` setting should be the publicly-accessible hostname of the
server nagios is running on, the port (if required), and the path the wsgi
script is running on. Since in the apache configuration example I direct the
request to nagifo only if the URI starts with ``/nagifo``, the ``external_url``
must include ``/nagifo``.


.. _Notifo: http://notifo.com
.. _Notifo user settings: http://notifo.com/user/settings
.. _Flask deployment guide: http://flask.pocoo.org/docs/deploying/

