tornado-demo -- a standard layout for Tornado apps
===============================================================================

## Description

tornado-boilerplate is an attempt to set up an convention for
[Tornado](http://www.tornadoweb.org/) app layouts, to assist in writing
utilities to deploy such applications. A bit of convention can go a long way.

This app layout is the one assumed by [buedafab](https://github.com/bueda/ops).

Tested with Tornado v3.2 

### Related Projects

[buedafab](https://github.com/bueda/ops)
[django-boilerplate](https://github.com/bueda/django-boilerplate)
[python-webapp-etc](https://github.com/bueda/python-webapp-etc)
[comrade](https://github.com/bueda/django-comrade)

## Acknowledgements

The folks at Mozilla working on the [next version of AMO](https://github.com/jbalogh/zamboni)
were the primary inspiration for this layout.

## Directory Structure

    tornado_demo/
        apps           #    项目应用
            foo         
                handlers/      # 逻辑
                    foo.py
                    base.py
                tasks.py    #   定时任务
                urls.py     #   子项目路由
        logconfig/  #   日志配置
        media/      #   静态文件
            css/
                vendor/
            js/
                vendor/
            images/
        requirements/   #   插件安装（解决生产环境与测试环境系统不一致导致插件版本不存在问题）
            common.txt  #   通用
            dev.txt         # 测试环境
            production.txt  # 生产环境
        templates/      #   模板
        environment.py  #   运行环境
        fabfile.py  
        app.py      #   系统入口
        settings.py     # 系统设置，全局变量
        urls.py     #   系统总路由

### handlers

All of your Tornado RequestHandlers go in this directory.

Everything in this directory is added to the `PYTHONPATH` when the
`environment.py` file is imported.

### lib

Python packages and modules that aren't really Tornado request handlers. These
are just regular Python classes and methods.

Everything in this directory is added to the `PYTHONPATH` when the
`environment.py` file is imported.

### logconfig

An extended version of the
[log_settings](https://github.com/jbalogh/zamboni/blob/master/log_settings.py)
module from Mozilla's [zamboni](https://github.com/jbalogh/zamboni).

This package includes an `initialize_logging` method meant to be called from the
project's `settings.py` that sets Python's logging system. The default for
server deployments is to log to syslog, and the default for solo development is
simply to log to the console.

All of your loggers should be children of your app's root logger (defined in
`settings.py`). This works well at the top of every file that needs logging:

    import logging
    logger = logging.getLogger('five.' + __name__)

### media

A subfolder each for CSS, Javascript and images. Third-party files (e.g. the
960.gs CSS or jQuery) go in a `vendor/` subfolder to keep your own code
separate.

### requirements

pip requirements files, optionally one for each app environment. The
`common.txt` is installed in every case.

Our Fabfile (see below) installs the project's dependencies from these files.
It's an attempt to standardize the location for dependencies like Rails'
`Gemfile`. We also specifically avoid listing the dependencies in the README of
the project, since a list there isn't checked programmatically or ever actually
installed, so it tends to quickly become out of date.

### templates

Project-wide templates (i.e. those not belonging to any specific app in the
`handlers/` folder). The boilerplate includes a `base.html` template that defines
these blocks:

#### <head>

`title` - Text for the browser title bar. You can set a default here and
append/prepend to it in sub-templates using `{{ super }}`.

`site_css` - Primary CSS files for the site. By default, includes
`media/css/reset.css` and `media/css/base.css`.

`css` - Optional page-specific CSS - empty by default. Use this block if a page
needs an extra CSS file or two, but doesn't want to wipe out the files already
linked via the `site_css` block.

`extra_head` - Any extra content for between the `<head>` tags.

#### <body>

`header` -Top of the body, inside a `div` with the ID `header`.

`content` - After the `header`, inside a `div` with the ID `content`.

`footer` - After `content`, inside a `div` with the ID `footer`.

`site_js` - After all body content, includes site-wide Javascript files. By
default, includes `media/js/application.js` and jQuery. In deployed
environments, links to a copy of jQuery on Google's CDN. If running in solo
development mode, links to a local copy of jQuery from the `media/` directory -
because the best way to fight snakes on a plane is with jQuery on a plane.

`js` - Just like the `css` block, use the `js` block for page-specific
Javascript files when you don't want to wipe out the site-wide defaults in
`site_js`.

#### TODO

This needs to be tested with Tornado's templating language. A quick
look at the documentation indicates that this basic template is compatible, but
none of our Tornado applications are using templates at the moment, so it hasn't
been tested.


### Files

#### environment.py

Modifies the `PYTHONPATH` to allow importing from the `apps/`, `lib/` and
`vendor/` directories. This module is imported at the top of `settings.py` to
make sure it runs for both local development (using Django's built-in server)
and in production (run through mod-wsgi, gunicorn, etc.).

#### fabfile.py

We use [Fabric](http://fabfile.org/) to deploy to remote servers in development,
staging and production environments. The boilerplate Fabfile is quite thin, as
most of the commands are imported from [buedafab](https://github.com/bueda/ops),
a collection of our Fabric utilities.

#### app.py

The main Tornado application, and also a runnable file that starts the Tornado
server.

#### settings.py

A place to collect application settings ala Django. There's undoubtedly a better
way to do this, considering all of the flak Django is taking lately for this
global configuration. For now, it works.

## Contributing

If you have improvements or bug fixes:

* Fork the repository on GitHub
* File an issue for the bug fix/feature request in GitHub
* Create a topic branch
* Push your modifications to that branch
* Send a pull request

## Authors

* [陈军辉](http://www.shaonian.site)
*  [Github](https://github.com/baqmxdsny)
