#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""
SimpleTranslate plugin for Pelican
===========================

This plugin add function, filter and tag to translate website in different
languages. The translation file is assumed to be in the Theme folder in a file
called translation.py which must contain a structure like:

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

if a translation is missing the string you tried to translate is returned

"""

from jinja2.exceptions import TemplateSyntaxError
from jinja2.ext import Extension
from jinja2 import nodes
from pelican import signals
import os


class TranslateExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['trans'])

    def __init__(self, environment):
        super(TranslateExtension, self).__init__(environment)
        self._args = []

    def parse(self, parser):
        lineno = parser.stream.next().lineno

        if parser.stream.skip_if('name:with'):
            _with = parser.parse_primary()
        else:
            _with = nodes.Const(None)
        if parser.stream.skip_if('name:from'):
            _from = parser.parse_primary()
        else:
            _from = nodes.Const(None)
        if parser.stream.skip_if('name:into'):
            _into = parser.parse_primary()
        else:
            _into = nodes.Const(None)

        body = parser.parse_statements(['name:endtrans', 'name:plural'], drop_needle=True)
        if not parser.stream.current.test('block_end'):
            plural_expr = parser.parse_primary()
            body.extend ( parser.parse_statements(['name:endtrans'], drop_needle=True) )
        else:
            plural_expr = nodes.Const(None)

        args = [_with, _from, _into, plural_expr, nodes.Const([y.data for x in body for y in x.nodes])]
        #print "argomenti1", args

        return nodes.CallBlock(self.call_method('_trans', args),
                               [], [], body).set_lineno(lineno)

    def _trans(self, _with, _from, _into, plural_expr, parts, caller):
        """Helper callback."""
        #print "argomenti2", _with, _from, _into, plural_expr, parts

        ret = caller().strip(' \r\n')
        parts = [x.strip(' \r\n') for x in parts]
        ret = parts[0]
        if (plural_expr is True) or (plural_expr>1):
            ret = parts[1]
        try:
            return self.do_translate(ret, _with, _into=_into, _domain=_from)
        except Exception, e:
            return ret + '<span style="display:none">'+e.message+'</span>'

def install_addition_template_function(generator):
    translator = TranslateExtension(generator.env)

    if os.path.exists(generator.theme+'/translation.py'):
        import imp
        domains = imp.load_source('translation', generator.theme+'/translation.py').domains
    else:
        domains = dict()

    def do_translate(_translate_string, *klist, **kargs):
        if '_into' not in kargs or kargs['_into'] is None:
            _into = generator.context['DEFAULT_LANG']
        else:
            _into = kargs['_into']

        if '_domain' not in kargs or kargs['_domain'] is None:
            _domain = 'translations'
        else:
            _domain = kargs['_domain']

        ret = domains                \
                .get(_domain, dict()) \
                .get(_into, dict())    \
                .get(_translate_string, _translate_string)
        if klist:
            try:
                ret = ret.format(klist)
            except KeyError:
                ret = ret.format(**klist[0])
        if kargs:
            ret = ret.format(**kargs)

        return ret

    translator.do_translate = do_translate
    generator.env.extensions['simpletranslate.simpletranslate.TranslateExtension'] = translator
    generator.env.filters['trans'] = do_translate
    generator.env.globals['trans'] = do_translate
    generator.env.globals['__'] = do_translate
    generator.env.globals['_'] = do_translate


def register():
    signals.generator_init.connect(install_addition_template_function)
