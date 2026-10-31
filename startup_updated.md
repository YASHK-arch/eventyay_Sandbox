```
```

# Start Eventyay with the Local Teamshifts Plugin (Windows)

Run these commands in PowerShell from the repository root. This Docker-based setup mounts the local `plugins/eventyay-teamshifts` checkout and serves Eventyay at `http://127.0.0.1:8000/`.

## One-Time Setup

1. Start Docker Desktop:

   ```powershell
   docker desktop start
   ```
2. Confirm `.env.dev` exists at the repository root. If it does not, create it from the development sample and configure its local values:

   ```powershell
   Copy-Item deployment/env.dev.sample .env.dev
   ```
3. Build the app image once, and again after changing the Dockerfile or Python dependencies:

   ```powershell
   docker compose build web
   ```

The app lockfile targets Linux and macOS, so run the app in Docker instead of syncing `app/.venv` on Windows.

## Start the Project

Run from the repository root:

```powershell
docker desktop start
docker compose up -d db redis

# Remove only web containers from this local setup, including a stopped one.
$oldWeb = docker ps -a --format '{{.Names}}' | Where-Object {
    $_ -eq 'eventyay-teamshifts-web' -or $_ -like 'eventyay-next-web-run-*'
}
if ($oldWeb) { docker rm -f $oldWeb }

# Check for another container that would prevent binding port 8000.
$portOwner = docker ps --filter publish=8000 --format '{{.Names}}'
if ($portOwner) { throw "Port 8000 is already used by: $($portOwner -join ', '). Stop that container before continuing." }

$pluginPath = (Resolve-Path .\plugins\eventyay-teamshifts).Path
$startupCommand = "uv pip install --python /usr/src/app/.venv/bin/python -e /usr/src/plugin-src && /usr/src/app/.venv/bin/python manage.py migrate && /usr/src/app/.venv/bin/python manage.py collectstatic --noinput && /usr/src/app/.venv/bin/python manage.py compress --force && /usr/src/app/.venv/bin/python manage.py shell -c 'from django.core.cache import cache; cache.clear()' && /usr/src/app/.venv/bin/python manage.py runserver 0.0.0.0:8000"

docker compose run -d --no-deps --name eventyay-teamshifts-web -p 8000:8000 -v "${pluginPath}:/usr/src/plugin-src" --entrypoint /bin/bash web -c $startupCommand
```

The separate `/usr/src/plugin-src` mount keeps the local plugin visible despite Compose's parent `/usr/src/plugins` mount. The custom entrypoint installs the mounted plugin, migrates, collects static files, builds compressed assets, clears stale development cache entries, and then starts Django.

Check startup logs and open the site:

```powershell
docker logs -f eventyay-teamshifts-web
```

Stop following the logs with `Ctrl+C`; the detached web container keeps running. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in the browser. The homepage should return HTTP 200 with its CSS loaded.

If the page is unstyled, rebuild the compressed assets and clear the development cache:

```powershell
docker exec eventyay-teamshifts-web /usr/src/app/.venv/bin/python manage.py collectstatic --noinput
docker exec eventyay-teamshifts-web /usr/src/app/.venv/bin/python manage.py compress --force
docker exec eventyay-teamshifts-web /usr/src/app/.venv/bin/python manage.py shell -c 'from django.core.cache import cache; cache.clear()'
```

## Stop the Project

```powershell
docker stop eventyay-teamshifts-web
docker compose stop db redis
```

Start it again by following **Start the Project**. Do not run `docker compose up -d` for the entire stack alongside this setup; it tries to start another web container on port 8000 and also starts unrelated video services.

## Notes

- `docker compose up -d db redis` starts dependencies on the Compose network; they do not need host ports published.
- A warning that `base` models have changes without a migration may appear during startup in this checkout. It is separate from Teamshifts startup; do not generate migrations as part of this procedure.
