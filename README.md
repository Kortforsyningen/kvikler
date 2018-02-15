# Kvikler

Prototype for the next generation of the Danish benchmark database.

## Usage

The package is at its infancy and is not much more than a *helloworld* script wrapped in
fancy scaffolding. After installation the `kvik` command line interface will be available:

```
> kvik --help
Usage: kvik [OPTIONS] COMMAND [ARGS]...

  Command line frontend to the kvikler database system.

Options:
  --help  Show this message and exit.

Commands:
  admin  Administrative tools for the kvikler database...
```

`kvik` will be expanded as work on the *kvikler* database system progresses.

## Installation

Clone or download the code from the GitHub repository and install the package with `pip` from
within the `kvikler` directory:

```
> pip install -e .
```

This will work on most systems. On Windows it is assumed that a somewhat complete OSGeo4W
installation is already available. Run the installation from the OSGeo4W shell.

Before using *kvikler* as configuration file is needed. It needs to be placed in your `HOME`
directory. On Windows that is typically `C:\Users\<yourusername>`. The configuration file
should be called `kvikler_settings.json`. Below is an example configuration file.

```json
{
    "connection":
    {
        "password": "<password>",
        "username": "<username>",
        "hostname": "<hostname>",
        "database": "<database>",
        "schema": "<schema>"
    }
}
```

## Testing

Run the test suite with:

```
python setup.py test
```

## Why "kvikler"?

The thing needs a name. One of the purposes of the database system is the ability to monitor the
movement of the sediment-rich ground in Denmark. Plastic clay is one of the big offenders when it
comes to sediments moving under their own weight. An extreme example of that is demonstrated in the
classic Norwegian documentary ["Kvikkleirskreddet i Rissa"](https://www.youtube.com/watch?v=26hooxzCGkY)(The quick clay landslide in Rissa).
The name is inspired by the quick clay in the documentary, albeit with the Danish spelling
"kvikler" since after all the software originates from Denmark.

But most importantly, *kvikler* is just a fun word to say!
