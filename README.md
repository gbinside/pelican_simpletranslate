SimpleTranslate plugin for Pelican
===========================

To install this plugin put it in your `plugins` folder (in a folser called `simpletranslate`) and add reference to the plugin into your pelican configuration file (tipically `pelicanconf.py`):

	PLUGINS = [
	...
	    'simpletranslate',
	...
	]

This plugin add function, filter and tag to translate website in different
languages. The translation file is assumed to be in the Theme folder in a file
called `translation.py` which must contain a structure like:

	domains = dict (
	    translations = { #default domain
	        'en':{
	          'last_article' : 'Last Article',
	          'last_article {x}' : 'Last Article {x}',
	          },
	        'it':{
	          'last_article' : 'Ultimo Articolo',
	          'last_article {x}' : 'Ultimo Articolo {x}',
	          'not found' : 'non trovato',
	          'apple':'mela',
	          'apples':'mele',
	          },
	        'fr':{
	          'last_article' : 'Dernier Article',
	          'last_article {x}' : 'Dernier Article {x}',
	          'not found' : u'pas trouv&eacute;',
	        },
	    },
	    app = {
	        'fr': {
	          'last_article' : 'Dernier Article -app-',
	          'last_article {x}' : 'Dernier Article {x} -app-',
	          'not found' : u'pas trouv&eacute; -app-',
	        }
	    }
	)

If a translation is missing the string you tried to translate is returned

Available sintax to translate strings

	{{ trans('last_article') }}
	
	{{ _('last_article') }}
	
	{{ __('last_article') }}
	
	{{ 'last_article'|trans|e }}
	
	{{ 'last_article {x}'|trans({'x':'ciao'})|e }}
	
	{{ 'last_article {x}'|trans(x = 'ciao')|e }}
	{% trans with {'x':'ciao'} from "app" into "fr" %}
	  last_article {x}
	{% endtrans %}
	{% endraw %}
	
	{% trans with {'x':'ciao'} from "app" into "fr" %}
	  last_article {x}
	{% endtrans %}
	
	{% trans with {'x':'ciao'} into "fr" %}
	  last_article {x}
	{% endtrans %}
	
	{% set apple_count = 1 %}
	{{ apple_count }} {% trans %}
	  apple
	  {% plural apple_count %}
	  apples
	{% endtrans %}
	
	{% set apple_count = 2 %}
	{{ apple_count }} {% trans %}
	  apple
	  {% plural apple_count %}
	  apples
	{% endtrans %}
	
	{% set apple_count = 3 %}
	{{ apple_count }} {% trans %}
	  apple
	  {% plural (apple_count>1) %}
	  apples
	{% endtrans %}
	
	{% trans with {'x':'not found'|trans} into "fr" %}
	  last_article {x}
	{% endtrans %}
	
	{% trans with {'x':('not found'|trans(_into="fr"))} into "fr" %}
	  last_article {x}
	{% endtrans %}
	
	{% trans into "fr" %}
	    not found
	{% endtrans %}

Why reinvent the wheel?
------------------------

Because the wheel included in Pelican is too big for me. Janja2 is used into Django as a realtime template system. In Pelican I have no need of performance because it's all statically generated. If my blog take 31 seconds instead of 30 to be generated (once a day), I can survive.
So I created this smaller wheel that don't need compilation of `mo` files into `po` files.
