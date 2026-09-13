# Third-party packages observed in the late repair phase

Binary packages remain outside the public archive. This directory keeps version/acquisition metadata and original notices where available.

| Package | Role |
|---|---|
| Cygwin e2fsprogs 1.44.5 and dependencies | Build/check compatible cache filesystem; offline userdata fsck trial |
| Android SDK Platform Tools 37.0.1 | Downloaded reference toolset; not the ADB instance used for the successful original connection |
| Rockchip ADB Driver 4.5 | Researched offline; not required to be installed for the successful connection |
| Google USB Driver r04 | Researched alternative; not installed in the successful path |

The historical working ADB 1.0.31 environment from AndroidTool 2.43 was an external dependency from the earlier phase and is not redistributed here.
