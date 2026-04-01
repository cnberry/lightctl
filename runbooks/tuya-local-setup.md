# Tuya Local Setup (Manual Steps)

Use this runbook when onboarding a new disposable/test Tuya device so `lightctl` can control it locally.

## Goal
Get these values for a device:
- local IP
- device ID
- local key
- protocol version
- switch datapoint (usually `1` for simple plugs)

## Recommended setup choice
Use the **Tuya Smart** app for test devices instead of an OEM-branded app. This makes key extraction and local control much easier.

## Manual steps

### 1. Pair the device in Tuya Smart
- Put the device into pairing mode.
- Add it in the **Tuya Smart** app.
- Give it a boring clear name, e.g. `TestPlug`.
- Make sure it joins the normal 2.4 GHz home Wi‑Fi.

### 2. Create a Tuya cloud project
- Go to `https://iot.tuya.com`
- Create/sign into a Tuya developer account.
- Create a cloud project (Smart Home is fine).
- Use the Western America / US data center if that matches the app/device.

### 3. Link the Tuya Smart app account to the project
- In the project, find the **Devices** area.
- Use **Link App Account** / **App Account** / QR-code linking.
- Connect the same Tuya Smart account that owns the device.
- Confirm the device shows up in the project device list.

### 4. Authorize cloud APIs
If the project has no API permissions, add at least:
- **IoT Core**
- **Smart Home Basic Service**

Without these, the API may return `No permissions` even if the device is visible in the web UI.

### 5. Add API IP whitelist entry
- In the Tuya cloud project, add the network's **public IPv4** to the API whitelist.
- For this environment, the IPv4 that worked was `203.0.113.10`.
- IPv6 was not accepted by Tuya in this flow.

### 6. Get the cloud credentials
From the project overview/details page, collect:
- **Access ID**
- **Access Secret**
- region/data center

### 7. Discover the device locally
From the repo machine:
```bash
source .venv/bin/activate
python -m tinytuya scan
```
This yields a local snapshot with:
- device IP
- device ID
- product key
- protocol version

### 8. Pull the local key via Tuya cloud
Once the project is linked, APIs are authorized, and IPv4 whitelist is set, use the linked account/project to fetch devices and keys.

For this workspace, an IPv4-only workaround was required when calling the Tuya API from Python because Tuya rejected IPv6-whitelist-less requests.

### 9. Record the device in `config/lights.json`
Add/update fields:
- `host`
- `device_id`
- `local_key`
- `protocol_version`
- `switch_dp`
- `mac` if known

Use meaningful house-facing names in config ids, e.g. `landscape-lights`, not OEM labels.

### 10. Verify local control
Use:
```bash
python3 lightctl.py status <device-id>
python3 lightctl.py on <device-id>
python3 lightctl.py off <device-id>
```

## Proven working examples
### TestPlug
- name: `TestPlug`
- host: `192.168.1.60`
- device_id: `replace-with-device-id`
- protocol_version: `3.3`
- switch_dp: `1`
- cloud function code: `switch_1`

### Landscape Lights
- config id: `landscape-lights`
- Tuya project/device label used during extraction: `Landscape Power`
- host: `192.168.1.50`
- device_id: `replace-with-device-id`
- protocol_version: `3.4`
- switch_dp: `1`

## Notes
- OEM apps may work as white-labeled Tuya apps, but user-facing names in tooling should be meaningful labels like `landscape-lights`, not vendor names.
- For unknown devices, `switch_dp` is often `1`, but always confirm with a working test device first.
- Do not commit real local keys to public repos.
