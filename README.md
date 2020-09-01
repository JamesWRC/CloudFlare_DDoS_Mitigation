# Cloudflare DDoS Mitigation / Rate Limiter
Helps prevent DDoS attacks from bad hosts and IPs. 
Acts as a free alternative to help reduce server load and cost for origin servers and serverless environments.

<h3 align="center">Cloudflare DDoS Mitigation</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/JamesWRC/CloudFlare_DDoS_Mitigation)
[![GitHub Issues](https://img.shields.io/github/issues/jameswrc/CloudFlare_DDoS_Mitigation.svg)](https://github.com/JamesWRC/CloudFlare_DDoS_Mitigation/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/JamesWRC/CloudFlare_DDoS_Mitigation.svg)](https://github.com/JamesWRC/CloudFlare_DDoS_Mitigation/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

</div>
---

## 📝 Table of Contents

- [Introduction](#introduction)
- [How can this help?](#how_this_can_help)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Install](#install)
- [Acknowledgments](#acknowledgments)

## Introduction <a name = "introduction"></a>
This utilizes the ability to create a Cloudflare Firewall rule, monitor activity and set rules to act on certain activity. 
This works on any account tier, especially free. Features will be developed slowly, this is mainly here to benefit my uses. I will added more user friendly interfaces and easier to use rules etc. This is open source for others to use and modify how they please. Hopefully someone finds this useful :)


## How can this help <a name = "how_this_can_help"></a>
I have designed this tool to help reduce the impact and costs involved when someone tries to knock your services offline or make you rack up huge serverless costs.
Hopefully some people find this usefully when designing their own sites and applications, so that this can help protect their applications from attacks. I have tried to design this to be light weight and easy to implement. 

#### DDoS Mitigation
This project helps mitigate flood based attacks from different addresses, that aim to use up server compute time and rack up server costs. Cloudflare does a great job of protecting sites, however there is often a little bit of a lag between an incoming attack and Cloudflare stopping it. This is due to the unpredictable nature of attacks, so Cloudflare does not want to block legit requests and ruining the experience of users. 

This tool enables you to fine tune and help block possible attacks a little more aggressively, to reduce the impact of an attack, and give you more control over the amount of requests your site should accept before actions are taken to help mitigate an attack.


#### Rate Limiter
Not only can this project help mitigate DDoS/Flood attacks, it can also act as a rate limiter for you site and resources. Configuring the tool to count the number of requests each IP is making, then you can easily rate limit your site, resources and/or your API! This can be very useful when your applications cost you money per request, or an API request is computationally expensive. Especially if you are utilizing Cloudflare workers where you are being billed each request, each KV action, each gigabyte of storage...


#### Block and filter access
This tool allows you to filter access from Autonomous System Number (ASN) or country. If an attack has different IP addresses all from the same country, you could enable a rule that a certain country may have a upper limit of requests, to help limit possible geographical based attacks. Another use case could be if you have specific content that may have copyright laws, and you want to ban a certain country from accessing your site / content. 


## Prerequisites <a name = "prerequisites"></a>
- Cloudflare.
  - any tire will do, even free.
- Docker installed on a server.
  - Can be your origin server, any other server **or even** a raspberry pi.

## Configuration <a name = "configuration"></a>
### Cloudflare
You will need to add some firewall settings.

1. Create a new firewall rule in your account.
2. Give the rule any name. For example you can name it 'Activity Logging'
3. Click 'Edit expression' and past the code bellow into the text field. (This simply just logs any and all requests to your site.)
```(http.request.method eq "GET") or (http.request.method eq "POST") or (http.request.method eq "PURGE") or (http.request.method eq "PUT") or (http.request.method eq "HEAD") or (http.request.method eq "OPTIONS") or (http.request.method eq "DELETE") or (http.request.method eq "PATCH")```
3. Finally chose the action, set this to 'Allow'.
4. Click 'Deploy'
5. Done!

What the above does simply enables cloudflare to log all activity to your site / web resources. This tool then queries these logs to then take actions if/when IP addresses make a certain amount of requests in a minute.


### Settings / preferences
In the code you will see a basic settings.json.
In this file you will need to provide your:
- Cloudflare API key
- Cloudflare email account
- The Cloudflare Zone ID you wish to use this tool with.

There are additional settings that come default (recommended) configurations. They are as follows:
- ```CF_API_TOKEN``` --> provide your [Cloudflare API key](https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys#12345682). 
- ```CF_EMAIL_ADDRESS``` --> Your Cloudflare accounts email.
- ```CF_ZONE_ID``` --> Your Cloudflare Zone ID.
- ```LOG_REQUEST_DELAY``` --> The amount of seconds to wait before making another request to Cloudflare logs.
- ```JS_CHALLENGE_LIMIT``` --> The number of requests in one minutes a host needs to make before it will be JavaScript challenged.
- ```CAPTCHA_CHALLENGE_LIMIT``` --> The number of requests in one minutes a host needs to make before it will be CAPTCHA challenged.
- ```BAN_LIMIT``` --> The number of requests in one minutes a host needs to make before it will be banned.
- ```NUM_JS_CHALLENGE_DAYS``` --> The number of days the JavaScript challenge will be in place for a host that has exceeded the ```CAPTCHA_CHALLENGE_LIMIT```.
- ```NUM_CAPTCHA_CHALLENGE_DAYS``` --> The number of days the CAPTCHA challenge will be in place for a host that has exceeded the ```CAPTCHA_CHALLENGE_LIMIT```.
- ```NUM_BAN_WEEKS``` --> The number of WEEKS the ban will be in place for a host that has exceeded the ```CAPTCHA_CHALLENGE_LIMIT```.
- ```UNDO_ACTION_EVERY_XTH_HOUR``` --> The number number of hours wait until actions are checked or removed.


### Install <a name = "install"></a>
- You will need to first [install docker for your machine / server](https://docs.docker.com/get-docker/)
- Now get the docker image:
```
Docker image is not ready yet, check back later or build image locally
```
- Build the container locally by running:
```sudo chmod +x buildDocker.sh && ./buildDocker.sh```
- Run the docker container:
```docker run cloudflare_ratelimiter```
- Configure to your needs.


## Acknowledgments <a name = "acknowledgments"></a>

* [Cloudflare documentation](https://api.Cloudflare.com/)
* [Cloudflare GraphQL API for firewall events](https://developers.cloudflare.com/analytics/graphql-api/tutorials/querying-firewall-events)

## Powered by <a name = "powered_by"></a>

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Python3](https://www.python.org) - Language used
* [Docker](https://docs.docker.com/get-docker/) - Orchestration
* [Cloudflare](https://www.Cloudflare.com) - Main web proxy service.