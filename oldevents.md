---
layout: page
title: Old Leagues and Tournaments
---

Old tournament and league event pages.

## Leagues

{% for node in site.pages %}
	{% if node.title != null %}
		{% if node.layout == "league" %}
			{% if node.active != true %}  
[{{ node.title }}]({{ node.url }})  
			{% endif %}
		{% endif %}
	{% endif %}
{% endfor %}

## Tournaments

{% for node in site.pages %}
	{% if node.title != null %}
		{% if node.layout == "tournament" %}
			{% if node.active != true %}     
[{{node.title}}]({{ node.url }})
			{% endif %}
		{% endif %}
	{% endif %}
{% endfor %}