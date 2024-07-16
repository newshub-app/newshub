* [:newspaper: newshub](#newspaper-newshub)
* [:sparkles: Features](#sparkles-features)
* [:rocket: Setup](#rocket-setup)
    * [:wrench: Configuration](#wrench-configuration)
    * [:whale: Docker](#whale-docker)
    * [:keyboard: Development](#keyboard-development)
* [:alarm_clock: Periodic tasks](#alarm_clock-periodic-tasks)
* [:copyright: License](#copyright-license)

---

# :newspaper: newshub

NewsHub is a news sharing platform that allows users to save links and have them shared
among members via periodic newsletters.

# :sparkles: Features

* Share interesting links with friends and teammates
* Send a periodic newsletter with a digest of the latest links
* API for programmatic access
* Browser extension to add links directly from the browser
* TODO: RSS feed reader
* TODO: AI-based links descriptions generation
* TODO: AI-based newsletter summary generation

# :rocket: Setup

## :wrench: Configuration

All the application settings are stored in the `newshub/settings.py` file, please refer to it and to the linked
documentation for each section to know more about them. To make deployment easier, the following settings
can also be defined using environment variables:

| Setting   | Default value   |
|-----------|-----------------|
| TODO      | TODO            |
| --------- | --------------- |

## :whale: Docker

NewsHub can be deployed as a docker container using the `ghcr.io/newshub-app/newshub` image, which is used
to power the main web application, as well as the Celery worker and scheduler used to run periodic tasks.

To deploy the whole software stack, the provided `docker-compose.yml` file can be used. Shared settings and
sensitive values are expected to be found in a `settings.env` file, which you can create using the provided
`settings.env.example` file as a template.

## :keyboard: Development

A `docker-compose.dev.yml` file is provided to extend the default compose file so that the environment is more
suitable for local development using the following command:

```text
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Running the application in development mode will:

* Mount the source code as a volume in the container
* Reload both the application and Celery workers when code changes
* Expose services ports to `localhost`:
    * 8000 (main web application)
    * 5432 (PostgreSQL)
    * 5672 (RabbitMQ)
    * 6379 (Redis)

# :alarm_clock: Periodic tasks

TODO

# :copyright: License

NewsHub is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NewsHub is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NewsHub. If not,
see <https://www.gnu.org/licenses/>.
