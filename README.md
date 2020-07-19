# CloudFlare DDoS Mitigation / Rate Limiter
Helps prevent DDoS attacks from bad hosts and IPs. 
Acts as a free alternative to help reduce server load and cost for origin servers and serverless environments.


## Introduction
This utilizes the ability to create a CloudFlare Firewall rule, monitor activity and set rules to act on certain activity. 
This works on any account tier, especially free. Features will be developed slowly, this is mainly here to benefit my uses. I will added more user friendly interfaces and easier to use rules etc. This is open source for others to use and modify how they please. Hopefully someone finds this useful :)


## How can this help
I have designed this tool to help reduce the impact and costs involved when someone tries to knock your services offline or make you rack up huge serverless costs.
Hopefully some people find this usefully when designing their own sites and applications, so that this can help protect their applications from attacks. I have tried to design this to be light weight and easy to implement. 

### Prerequisites
- CloudFlare.
  - any tire will do, even free.
- Docker installed on a server.
  - Can be your origin server **or** any other server.


### DDoS Mitigation
This project helps mitigate flood based attacks from different addresses, that aim to use up server compute time and rack up server costs. CloudFlare does a great job of protecting sites, however there is often a little bit of a lag between an incoming attack and cloudflare stopping it. This is due to the unpredictable nature of attacks, so CloudFlare does not want to block legit requests and ruining the experience of users. 

This tool enables you to fine tune and help block possible attacks a little more aggressively, to reduce the impact of an attack, and give you more control over the amount of requests your site should accept before actions are taken to help mitigate an attack.


### Rate Limiter
Not only can this project help mitigate DDoS/Flood attacks, it can also act as a rate limiter for you site and resources. Configuring the tool to count the number of requests each IP is making, then you can easily rate limit your site, resources and/or your API! This can be very useful when your applications cost you money per request, or an API request is computationally expensive. Especially if you are utilizing CloudFlare workers where you are being billed each request, each KV action, each gigabyte of storage...


### Block and filter access
This tool allows you to filter access from Autonomous System Number (ASN) or country. If an attack has different IP addresses all from the same country, you could enable a rule that a certain country may have a upper limit of requests, to help limit possible geographical based attacks. Another use case could be if you have specific content that may have copyright laws, and you want to ban a certain country from accessing your site / content. 

### Install
- You will need to first [install docker for your machine / server](https://docs.docker.com/get-docker/)
- Now get the docker image:
```
Docker image is not ready yet, check back later or build image locally
```
- Run the docker container:
```
Have not made or named the docker container, check back soon :)
```
- Configure to your needs.

## Configuration
- Nothing just yet.


## Powered by

* [Django](https://www.djangoproject.com) - The web framework used
* [Python3](https://www.python.org) - Language used
* [Docker](https://docs.docker.com/get-docker/) - Orchestration
* [CloudFlare](https://www.cloudflare.com) - Main web proxy service.

## Acknowledgments

* [CloudFlare documentation](https://api.cloudflare.com/)
