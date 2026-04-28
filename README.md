<!-- SPONSOR-START -->
---

<div align="center">

### 🌐 Need Proxies? Check out my services

<a href="https://vaultproxies.com" target="_blank" rel="noopener noreferrer">
  <img src="https://i.imgur.com/TF165pP.gif" alt="VaultProxies">
</a>
<p></p>

<table>
  <tr>
    <th>Service</th>
    <th>Pricing</th>
    <th>Features</th>
  </tr>
  <tr>
    <td><b><a href="https://vaultproxies.com" target="_blank" rel="noopener noreferrer">🔮 VaultProxies</a></b></td>
    <td><code>$1.00/GB</code> residential</td>
    <td>Residential · IPv6 · Residential Unlimited · Datacenter</td>
  </tr>
  <tr>
    <td><b><a href="https://nullproxies.com" target="_blank" rel="noopener noreferrer">🌑 NullProxies</a></b></td>
    <td><code>$0.75/GB</code> residential</td>
    <td>Residential · Residential Unlimited · DC Unlimited · Mobile Proxies</td>
  </tr>
  <tr>
    <td><b><a href="https://strikeproxy.net" target="_blank" rel="noopener noreferrer">⚡ StrikeProxy</a></b></td>
    <td><code>$0.75/GB</code> residential</td>
    <td>Residential · Residential Unlimited · DC Unlimited · Mobile Proxies</td>
  </tr>
</table>
</div>

<!-- SPONSOR-END -->

<div align="center">
 
  <h2 align="center">Cyberious API</h2>
  <p align="center">
    The API that I use for licensing, hardware ID (HWID) management, user verification, and Sellix order integration.
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Licensing-API/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Licensing-API/issues">💡 Request Feature</a>
  </p>
</div>

### ⚙️ Installation

- Requires: `Python 3.10+`
- Install the requirements: `pip install -r requirements.txt`
- Start the application: `python app.py`

---

### 🔥 Features

- **HWID Management**:
  - **Check HWID Status**: `/hwid` - Check if HWID is whitelisted or blacklisted.
  - **Register User**: `/register` - Register a new user with license and update HWID status.
  - **Verify User**: `/verify_user` - Verify user based on HWID.
  - **Check If Paused**: `/check_if_paused` - Check if a user's access is paused (useful for license pause).
  - **Check User Expiry**: `/check_user_expiry` - Check user expiry status.

- **Sellix Order Integration**:
  - **Sellix Webhook**: `/sellix` - Validate Sellix webhook signatures, creates a license and update order status and durations based on product titles.

- **User Verification & Status**:
  - **Get Latest Version**: `/get_latest` - Get the latest version of the launcher.
  - **Download Launcher**: `/download/launcher` - Provide access to the latest launcher version.
  - **Download Cyberious**: `/download/cyberious` - Control access to downloads based on HWID (license) authorization.

- **Other Endpoints**:
  - **Home**: `/` - Welcome message with API status and information.

---

### ❗ Disclaimers

- The project is under development and certain features might not be fully functional.
- Ensure to set up your Sellix webhook secret and whitelisted IP address properly in the variables section of the code.
- Use this project at your own risk. The author is not responsible for any issues that may arise from using this code.

---

### 📜 ChangeLog

```diff
v1.0.0 ⋮ 6/9/2024
! Initial release
```
<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Licensing-API.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Licensing-API.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Licensing-API.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
