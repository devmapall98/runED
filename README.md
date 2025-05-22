# runED

![GitHub Issues or Pull Requests]
![GitHub Release]
![GitHub Commits since last release]

**runED** was made in an effort to streamline launching of Elite Dangerous and all of the additional apps ([EDMC], [VoiceAttack], [EDEngineer] to name a few) for my own convenience.

If you don't need to launch anything **elevated** ("as admin"), then *rfvgyhn's* [min-ed-launcher] is probably a ***much*** better choice.

> **NOTE:** *They are not exclusive - you can totally use this to run min-ed-launcher, and there may be [some](#faq) situations where you may actually want to do that.*

## Table of Contents

- [Installation]
- [Configuration]
- [Some notes]
- [FAQ]
- [License]

## Installation

1. Download the [latest version] of runED.
2. Extract the .zip archive anywhere.
3. Start runED.
4. Done!

## Configuration

runED can be configured by editing its config file (located at `%APPDATA%\runED\config.yaml`). Unfortunately, for now, there is no way to configure it without editing the config manually. This will be remediated in a later version.

An example config file should look something like this:
```yaml
apps:
- enabled: true
  forceKill: false
  name: App1
  path: C:\Path\To\App1.exe
  vr: false
- enabled: true
  forceKill: true
  name: App2
  path: C:\Path\To\App2.exe
  vr: true

settings:
  ...
```

### How to add new applications for runED to manage

Each application managed by runED has its own configuration that looks like this:
```yaml
- enabled: true
  forceKill: false
  name: App1
  path: C:\Path\To\App1.exe
  vr: false
```

Here is an explanation of these settings:
- **enabled**: set to `true` if you want runED to manage the app, `false` if you want to temporarily disable it.
- **forceKill**: set to `true` if the app doesn't exit properly with runED even though `settings: closeAppsOnExit` is set to `true`
- **name**: name of the application - can be any name you want
- **path**: full path to the application executable
- **vr**: set to `true` if during setup you agreed to having a separate list of applications to manage with runED when using VR and you want the application to run when launching Elite Dangerous in VR, set to `false` to run the app only when playing in "desktop mode"

If you want to add another application to runED:
1. Copy the settings for the first app that you have set up on first launch of runED.
2. Change the `path` to point to the application executable.
3. Edit the rest of the settings to your liking.
4. Save & close the config file.
5. Done!

### What about other runED settings?

Sections `settings` and `vrSettings` are configured on first launch of runED. It is strongly recommended to delete the config file entirely, open runED and let it go through first launch setup to change these settings until a way to configure them from within the app gets implemented.

## Some notes

- The app itself doesn't need elevated privileges, as long as you don't place it in a protected folder (like `C:\Program Files\` or something like that), *however* some other applications that you may want to launch using this tool **will** require elevation. As I didn't find a way to elevate only a single app without showing the UAC prompt for each app that would require it, I opted to give you the option to trust the app and run the entirety of it elevated, along with everything you run through it. If you don't trust me and the app then all you have to do is keep the "Run elevated" setting off.
- In order to close programs the app will create `.bat` files inside the runED root folder, all named after the apps the user wishes to run, with contents like `taskkill /IM application.exe`, then it will quickly dispose of those files. Some antivirus programs may flag this. [Here is the exact function that does that] if that worries you and you want to take a look and make sure it is safe.

## FAQ

<details>

<summary>Q: "Why did you make this? Are you too lazy to click a bunch of apps before you launch the game?"</summary>

> **A:** Yes 🗿 But also it got to the point where I'm launching **8** (!!!) different applications alongside Elite Dangerous every time I want to play the game (because the game itself is really bad at giving you important information like market prices, locations of tech brokers etc.), and that is without taking into consideration which apps I want running when playing in VR and which ones when I play on the desktop. This app aims to alleviate *some* of that pain.
</details>

<details>

<summary>Q: "min-ed-launcher (great app btw, highly recommend it) exists already, why would I use this?"</summary>

> **A:** Nobody stops you from using [min-ed-launcher], hell, I use this app to launch some applications, and then use min-ed-launcher to launch others. They are both compatible with each other as long as you don't try to run the same application using both.
>
> Why would you want to run [min-ed-launcher] using this? In my case it was to automate turning on VoiceAttack and EDCoPilot along with the rest of the apps. For some reason, on my system these two just don't behave well without elevation \(╯°□°）╯︵ ┻━┻
</details>

<details>

<summary>Q: "Will this get updated soon since X changed and Y now doesn't work?"</summary>

> **A:** This honestly 100% depends on whether or not I'm hyper-focused on playing ED at the moment.
>
> *Soon?* **Doubt it.** *Ever?* **Most probably.**
>
> Please check date of last commit to see if this is still maintained - worst case scenario this will just stop working on a new update of Elite or something, if so then ping me an issue.
</details>

<details>

<summary>Q: "Man, this code stinks, I could write better code when I was a teenager1!!"</summary>

> **A:** High chance this is a correct statement.
</details>

<details>

<summary>Q: "This doesn't work with `APP NAME HERE`, can you fix that?"</summary>

> **A:** File an issue on github and I'll have a look at it 👀
</details>

<details>

<summary> Q: "Dude, it would be so cool if this app also did this and that and had a feature where it does this and shows you that as well!" </summary>

> **A:** Yea, that'd be cool
</details>

## License

This entire project is **[UNLICENSED]** - I don't care what you do with it and how. There is no "but" to that statement.

To learn more visit <https://unlicense.org/>

[GitHub Issues or Pull Requests]: https://img.shields.io/github/issues/devmapall98/runED
[GitHub Release]: https://shields.io/github/v/release/devmapall98/runED?include_prereleases&sort=semver&label=latest%20version&link=https%3A%2F%2Fgithub.com%2Fdevmapall98%2FrunED%2Freleases%2Flatest
[GitHub Commits since last release]: https://img.shields.io/github/commits-since/devmapall98/runED/latest/main

[Installation]: #installation
[Configuration]: #configuration
[FAQ]: #faq
[Some notes]: #some-notes
[License]: #license

[EDMC]: https://github.com/EDCD/EDMarketConnector
[VoiceAttack]: https://voiceattack.com/
[EDEngineer]: https://github.com/msarilar/EDEngineer
[min-ed-launcher]: https://github.com/rfvgyhn/min-ed-launcher
[UNLICENSED]: /UNLICENSE
[Here is the exact function that does that]: /libs/classes.py#L39
[latest version]: https://github.com/devmapall98/runED/releases/latest
