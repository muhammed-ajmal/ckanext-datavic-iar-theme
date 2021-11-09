# ckanext-datavic-iar-theme

A custom CKAN theme for the Data.Vic Data Directory (IAR).

## Installation

Add this repository as a sub-module to your main project repository:

        git submodule add git@github.com:salsadigitalauorg/ckanext_datavic_iar_theme.git ckan/default/src/ckanext-datavic-iar-theme

Activate the Python virtual environment:

        . /app/ckan/default/bin/activate

Install the CKAN extension:

        cd /app/ckan/default/src/ckanext-datavic-iar-theme

        python setup.py develop
        
*Add* `datavic_iar_theme` to plugins in /app/ckan/default/ckan.ini

        ckan.plugins = [...existing plugins...] datavic_iar_theme

Restart CKAN

        paster serve /app/ckan/default/development.ini

Or... Restart docker:

        docker-compose restart ckan
## CSS & Grunt

This theme adds a CSS resource to CKAN via the `fanstatic` dir:

        ~/ckanext-datavic-iar-theme/ckanext/datavic_iar_theme/fanstatic/datavic_iar_theme.css

This CSS file is generated through a basic `grunt` configuration in:

        ~/ckanext-datavic-iar-theme/ckanext/datavic_iar_theme/grunt

CD into that directory and run `npm install` to install grunt and its dependencies.
Install grunt cli globally `npm install -g grunt-cli`

Then compile the `.scss` files in the `ckanext-datavic-iar-theme/ckanext/datavic_iar_theme/grunt/sass` dir using:

        grunt
