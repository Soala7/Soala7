<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:001F54,50:005CFF,100:00BFFF&height=230&section=header&text=SOALA%20AMACHREE&fontSize=54&fontColor=ffffff&fontAlignY=34&desc=MECHATRONICS%20%7C%20SYSTEMS%20%7C%20ROBOTICS%20%7C%20AI&descAlignY=57&descSize=18&animation=fadeIn" width="100%"/>

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=21&duration=2800&pause=700&color=00BFFF&center=true&vCenter=true&width=950&lines=Mechatronics+Engineering+Student;Systems+%26+Software+Developer;Building+Gorgon+VirtualOS;Operating+Systems+%7C+Virtualization+%7C+Computer+Architecture;Robotics+%7C+AI+%7C+Embedded+Systems;Software+%E2%86%92+Systems+%E2%86%92+Hardware;Turning+ideas+into+working+systems"/>

<br><br>

<img src="https://komarev.com/ghpvc/?username=Soala7&label=PROFILE+VIEWS&color=005CFF&style=for-the-badge"/>
<img src="https://img.shields.io/github/followers/Soala7?style=for-the-badge&logo=github"/>
<img src="https://img.shields.io/github/stars/Soala7?style=for-the-badge"/>

</div>

---

# ⚡ SYSTEM STATUS

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=17&duration=1800&pause=400&color=00BFFF&center=true&vCenter=true&width=850&lines=%5BSYSTEM%5D+Engineering+environment+initialized;%5BCPU%5D+Systems+development+%5BONLINE%5D;%5BOS%5D+Gorgon+kernel+development+%5BIN+PROGRESS%5D;%5BVM%5D+QEMU%2FKVM+virtualization+%5BACTIVE%5D;%5BAI%5D+Machine+learning+%5BACTIVE%5D;%5BROBOTICS%5D+Embedded+systems+%5BACTIVE%5D;%5BHARDWARE%5D+Mechatronics+%5BONLINE%5D"/>

</div>

> **Build it. Break it. Understand it. Build it better.**

I'm **Soala Amachree**, a Mechatronics Engineering student interested in the intersection of **software, computer systems, electronics, intelligence and machines**.

I don't want to only use technology.

I want to understand **what happens underneath it** — from software and circuits to processors, memory, operating systems, robots and intelligent machines.

My goal is to become an engineer capable of moving across the stack:

**Software → Systems → Electronics → Embedded → AI → Robotics → Machines**

---

# 🧠 HOW I THINK

```text
                    HUMAN IDEA
                        │
                        ▼
               ┌────────────────┐
               │   SOFTWARE     │
               │   AI / APPS    │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │    SYSTEMS     │
               │  OS / RUNTIME  │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │  COMPUTER ARCH │
               │ CPU / MEMORY   │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │    EMBEDDED    │
               │ ELECTRONICS    │
               └───────┬────────┘
                       │
                       ▼
               ┌────────────────┐
               │    ROBOTICS    │
               │    MACHINES    │
               └────────────────┘
```

I like understanding systems **from the inside out**.

---

# 🖥️ GORGON — VIRTUALOS

<div align="center">

<img src="https://img.shields.io/badge/PROJECT-GORGON-001F54?style=for-the-badge&logo=linux&logoColor=white"/>
<img src="https://img.shields.io/badge/PHASE-2%20%7C%20REAL%20OS%20DEVELOPMENT-005CFF?style=for-the-badge"/>
<img src="https://img.shields.io/badge/FOCUS-KERNEL%20%7C%20VIRTUALIZATION%20%7C%20SYSTEMS-00BFFF?style=for-the-badge"/>

</div>

**Gorgon is my main systems project.**

It began as a Python/Pygame operating-system simulator.

Phase 1 proved the **desktop and user experience**.

Phase 2 is about building the **actual operating system underneath it**.

The goal is not to create a fake desktop.

The goal is to understand and build the layers that make a real computer system work.

---

## Phase 1 — VirtualOS Simulator ✅

The first version explored the operating-system experience in Python:

```text
┌────────────────────────────────────┐
│          VIRTUAL DESKTOP           │
├────────────────────────────────────┤
│                                    │
│  Window Management                 │
│  File Explorer                     │
│  Terminal / Shell                  │
│  Text Editor                       │
│  Application System                │
│  Virtual Filesystem                │
│  Persistent Storage                │
│  System Services                   │
│                                    │
└────────────────────────────────────┘
```

Phase 1 is now the **UX reference and experimental environment** for the real system.

---

# ⚙️ Phase 2 — Real Gorgon OS 🚧

Gorgon Phase 2 is being built around a real bootable x86-64 operating-system architecture.

```text
HOST COMPUTER
      │
      ▼
┌──────────────────────┐
│   GORGON LAUNCHER    │
│        C++           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      QEMU + KVM      │
│                      │
│  Virtual CPU         │
│  Virtual RAM         │
│  Virtual Disk        │
│  VirtIO Network      │
│  VirtIO GPU          │
│  Virtual Devices     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   GORGON BOOTLOADER  │
└──────────┬───────────┘
           │
           ▼
┌─────────────────────────────┐
│       GORGON KERNEL         │
├─────────────────────────────┤
│ CPU / Architecture          │
│ Memory Management           │
│ Virtual Memory / Page Tables│
│ Processes / Threads         │
│ Preemptive Scheduler        │
│ Interrupts                  │
│ Drivers / HAL               │
│ VFS / Filesystems           │
│ Networking                  │
│ IPC                         │
│ System Calls                │
│ Security / Isolation        │
└──────────────┬──────────────┘
               │
               ▼
   ┌─────────────────────────────┐
   │        GORGON INIT          │
   └──────────────┬──────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│             USERSPACE              │
├────────────────────────────────────┤
│ Desktop                            │
│ Window System / Compositor         │
│ Applications                       │
│ System Services                    │
│ Gorgon libc                        │
│ POSIX-oriented Environment         │
│ Runtimes                           │
│ Sandboxes / Containers             │
│ Linux ABI Compatibility            │
└────────────────────────────────────┘
```

### The important distinction

```text
GORGON NATIVE PROGRAM
        │
        ▼
 GORGON ABI / API
        │
        ▼
 GORGON KERNEL


POSIX SOFTWARE
        │
        ▼
   GORGON LIBC
        │
        ▼
 GORGON SYSCALLS
        │
        ▼
 GORGON KERNEL


LINUX SOFTWARE
        │
        ▼
 LINUX ABI COMPATIBILITY
        │
        ▼
 GORGON KERNEL
```

**POSIX compatibility helps software portability, but it does not automatically make Gorgon a Linux system.**

Linux compatibility will therefore be treated as a separate compatibility layer.

---

# 🧩 GORGON DEVELOPMENT STRATEGY

Gorgon is being developed through four major stages.

```text
┌─────────────────────────────────────┐
│  STAGE 1 — CORE KERNEL              │
│                                     │
│  Bootloader                         │
│  x86-64                             │
│  Memory                             │
│  Interrupts                         │
│  Processes                          │
│  Scheduler                          │
│  Drivers                            │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  STAGE 2 — USERSPACE FOUNDATION     │
│                                     │
│  Syscalls                           │
│  IPC                                │
│  VFS                                │
│  Filesystem                         │
│  Gorgon libc                        │
│  Static ELF                         │
│  Init                               │
│  Shell / Utilities                  │
│  POSIX-oriented APIs                │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  STAGE 3 — GRAPHICS & DESKTOP       │
│                                     │
│  VirtIO-GPU                         │
│  Framebuffers / Surfaces            │
│  Window System                      │
│  Compositor                         │
│  UI Framework                       │
│  Asset Manager                      │
│  Settings Service                   │
│  Desktop                            │
│  File Explorer                      │
│  Terminal                           │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  STAGE 4 — ECOSYSTEM & COMPATIBILITY│
│                                     │
│  Networking                         │
│  Audio                              │
│  Sandboxing / Containers            │
│  Python Runtime                     │
│  Lightweight Web Engine             │
│  Media / FFmpeg                     │
│  Linux ABI Compatibility            │
│  Dynamic Linking                    │
│  Chromium                           │
│  Real Hardware                      │
└─────────────────────────────────────┘
```

---

# 🎨 GORGON UI & ASSET SYSTEM

Gorgon isn't just about the kernel.

The userspace is intended to have a **custom desktop environment and graphics stack**.

### System Assets

```text
/system/
├── assets/
│   ├── icons/
│   ├── wallpapers/
│   ├── fonts/
│   ├── ui/
│   └── themes/
│
└── ...
```

The system asset layer will support:

* Custom icons
* Wallpapers
* UI graphics
* Transparent PNG assets
* High-resolution images
* Dynamic fonts
* Themes
* Rounded UI elements
* Alpha blending

The Gorgon UI library is planned to use technologies such as:

`stb_image` · `stb_truetype` · `FreeType`

where appropriate.

---

# ⚙️ DYNAMIC SETTINGS

System configuration should not be hardcoded into applications.

Gorgon will have a centralized settings architecture:

```text
                 SETTINGS APP
                       │
                       ▼
              ┌─────────────────┐
              │ SETTINGS SERVICE│
              └────────┬────────┘
                       │
                      IPC
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   DESKTOP SERVICE             COMPOSITOR
          │                         │
          └────────────┬────────────┘
                       ▼
                LIVE UI UPDATE
```

Possible configuration includes:

* Wallpaper
* Accent colors
* Themes
* Icon sets
* Window opacity
* UI preferences
* Desktop behavior
* User preferences

Changes should be applied **live without restarting the desktop** whenever practical.

---

# 🖼️ GORGON GRAPHICS ARCHITECTURE

The compositor should sit between applications and the actual display hardware.

```text
APPLICATION
     │
     ▼
GORGON GUI / GRAPHICS API
     │
     ▼
WINDOW SURFACE
     │
     ▼
COMPOSITOR
     │
     ├── Damage Tracking
     ├── Alpha Blending
     ├── Windows
     └── Desktop
     │
     ▼
RENDERER
     │
     ▼
VIRTIO-GPU / PHYSICAL GPU
```

The goal is to avoid making every application directly manipulate raw framebuffer memory.

SDL2 can still be ported later as a **userspace library/compatibility layer**, but it is not the foundation of Gorgon's graphics architecture.

---

# 💾 STORAGE & USERSPACE

Gorgon will eventually provide:

```text
Application
     │
     ▼
Gorgon libc / API
     │
     ▼
System Calls
     │
     ▼
VFS
     │
     ├── Gorgon Filesystem
     ├── Device Files
     └── Future Filesystem Drivers
     │
     ▼
Storage Driver
     │
     ▼
VirtIO / NVMe / AHCI
```

Early userspace programs will prioritize **static ELF executables**.

Dynamic linking and shared libraries come later once the fundamental execution environment is stable.

---

# 📦 SANDBOXING & CONTAINERS

Gorgon will eventually include a lightweight isolation system inspired by concepts such as:

* FreeBSD Jails
* `chroot`
* Process isolation
* Filesystem namespaces
* Resource limits
* Permission boundaries

The goal is a lightweight **Gorgon sandbox/container subsystem**, not simply a `chroot` wrapper.

```text
GORGON KERNEL
      │
      ├───────────────┐
      │               │
      ▼               ▼
  NORMAL APP       SANDBOX
                      │
                ┌─────┴─────┐
                │           │
             Filesystem   Process
             Isolation    Isolation
```

Containers share the Gorgon kernel.

Virtual machines have their own kernels.

---

# 🌐 NETWORKING & RUNTIMES

The long-term userspace environment is intended to support:

```text
                GORGON
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
   Native Apps   Runtimes   Services
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
       Python    Web     Media
                  Engine
                   │
                   ▼
              Chromium
```

The order matters.

Rather than attempting Chromium immediately, the system will first establish:

**Networking → Graphics → Window System → Runtime → Dynamic Linking → Linux Compatibility → Chromium**

Chromium is intended to become a major **real-world validation target** for the operating system.

---

# 🖥️ PHYSICAL HARDWARE

QEMU/KVM is the development environment — **not Gorgon's hardware dependency**.

The architecture is intended to eventually support real x86-64 machines.

```text
               GORGON
                 │
        HARDWARE ABSTRACTION
                 │
       ┌─────────┼───────────┐
       ▼         ▼           ▼
     QEMU      LAPTOP     DESKTOP
     VirtIO     Drivers     Drivers
       │         │           │
       └─────────┼───────────┘
                 ▼
              HARDWARE
```

The driver architecture will eventually cover areas such as:

* VirtIO
* PCI
* ACPI
* AHCI / SATA
* NVMe
* xHCI / USB
* UEFI GOP / framebuffer
* Networking
* Audio
* Physical GPUs

**UEFI is the primary modern physical boot target**, with legacy BIOS/CSM potentially supported as an additional path.

The long-term goal is to boot Gorgon from **USB and physical storage**, not only inside QEMU.

---

# 🧪 ENGINEERING STACK

## Languages

<div align="center">

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="48"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg" width="48"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/cplusplus/cplusplus-original.svg" width="48"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="48"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="48"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="48"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-original.svg" width="48"/>

</div>

### Systems

`C` · `C++` · `Assembly` · `Linux` · `GCC` · `GDB` · `QEMU` · `KVM` · `Docker` · `CMake` · `SDL2`

### Operating Systems

`Kernel Development` · `x86-64` · `ELF` · `Bootloaders` · `Memory Management` · `Virtual Memory` · `Interrupts` · `Processes` · `Scheduling` · `VFS` · `Drivers` · `System Calls` · `IPC`

### AI

`Python` · `PyTorch` · `TensorFlow` · `OpenCV` · `Machine Learning` · `Computer Vision` · `Reinforcement Learning`

### Robotics & Engineering

`Arduino` · `Embedded Systems` · `Electronics` · `KiCad` · `CAD` · `Fusion 360` · `Automation` · `Robotics`

### Development

`Git` · `GitHub` · `VS Code` · `React` · `Tailwind` · `Flask` · `Django`

---

# 🔬 CURRENTLY EXPLORING

```text
┌────────────────────────────────────────────┐
│             CURRENT LEARNING QUEUE         │
├────────────────────────────────────────────┤
│                                            │
│  > Advanced C                              │
│  > C++                                     │
│  > Assembly                                │
│  > Computer Architecture                   │  
│  > Operating System Development            │
│  > Linux System Programming                │
│  > QEMU / KVM Virtualization               │
│  > ELF & Toolchains                        │
│  > Memory Management                       │
│  > Embedded Systems                        │
│  > Robotics                                │
│  > Artificial Intelligence                 │
│  > Computer Vision                         │
│  > Reinforcement Learning                  │
│  > Rust                                    │
│  > ROS 2                                   │
│  > Embedded Linux                          │
│  > Containers & Sandboxing                 │
│                                            │
└────────────────────────────────────────────┘
```

---

# 🚀 PROJECTS

| Project                         | Description                                                                                          |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 🖥️ [**Gorgon simulator**](https://github.com/Soala7/Gorgon-OS-Virtual-Simulator) | A Python simulator into a bootable x86-64 operating system |
| 🌌 **Project Hollow**           | Long-term exploration of intelligent, secure and developer-focused computing environments            |
| 🐍 [**AI Snake**](https://github.com/Soala7/Snake-AI) | Reinforcement-learning Snake agent using Deep Q-Learning                                             |
| ♟️ [**Python Chess**](https://github.com/Soala7/Chess-game-2.0) | Chess application exploring game logic and AI                                                        |
| 🎓 **School Management System** | Student records, grading and academic management                                                     |
| 🤖 **AI Projects**              | Machine learning, computer vision and intelligent-system experiments                                 |
| 🔧 **Electronics Projects**     | Embedded systems and hardware experimentation                                                        |

---

# 🧭 ENGINEERING JOURNEY

```text
2024
 │
 ├── Python
 ├── Programming Fundamentals
 └── First Software Projects
       │
       ▼
2025
 │
 ├── Applications & Games
 ├── AI & Computer Vision
 ├── Electronics
 └── Engineering Projects
       │
       ▼
2026
 │
 ├── Mechatronics Engineering
 ├── C / C++
 ├── Assembly
 ├── Linux
 ├── Computer Architecture
 ├── Virtualization
 ├── QEMU / KVM
 ├── Operating Systems
 ├── Gorgon
 ├── AI
 └── Robotics
       │
       ▼
 FUTURE
 │
 ├── Advanced OS Development
 ├── Robotics
 ├── AI
 ├── Embedded Systems
 ├── Intelligent Machines
 └── Engineering Startups
```

---

# ⚙️ ENGINEERING PHILOSOPHY

I like learning technology from the **inside out**.

```text
              APPLICATION
                   ▲
                   │
                RUNTIME
                   ▲
                   │
              OPERATING
                SYSTEM
                   ▲
                   │
                 KERNEL
                   ▲
                   │
            COMPUTER ARCH.
                   ▲
                   │
                HARDWARE
                   ▲
                   │
             PHYSICAL WORLD
```

The deeper I go, the more interesting it becomes.

I don't want to memorize how systems work.

I want to **build enough of them to understand why they work.**

---

# 🎯 WHERE I'M GOING

I don't want to be restricted to only software or only hardware.

I want to become an engineer who can move between:

**Code → Systems → Electronics → Embedded → AI → Robotics → Machines**

and understand how those layers interact.

Eventually, I want to build systems where those disciplines aren't separate projects.

They're **one integrated system**.

---

# 📊 GITHUB

<div align="center">

<a href="https://github.com/Soala7">

<img height="180" src="https://github-readme-stats.vercel.app/api?username=Soala7&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&bg_color=0D1117&title_color=00BFFF&icon_color=005CFF&text_color=FFFFFF"/>

<img height="180" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Soala7&layout=compact&langs_count=8&hide_border=true&bg_color=0D1117&title_color=00BFFF&text_color=FFFFFF"/>

</a>

<br><br>

<img src="https://streak-stats.demolab.com?user=Soala7&theme=dark&hide_border=true&background=0D1117&ring=00BFFF&fire=005CFF&currStreakLabel=00BFFF"/>

<br><br>

<img src="https://github-profile-trophy.vercel.app/?username=Soala7&theme=algolia&no-frame=true&no-bg=true&row=2&column=4"/>

</div>

---

# 📡 CONNECT

<div align="center">

<a href="mailto:nigaamace@gmail.com">
<img src="https://img.shields.io/badge/Email-005CFF?style=for-the-badge&logo=gmail&logoColor=white"/>
</a>

<a href="https://github.com/Soala7">
<img src="https://img.shields.io/badge/GitHub-001F54?style=for-the-badge&logo=github&logoColor=white"/>
</a>

<a href="https://www.linkedin.com/in/soala-amachree">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>

<a href="https://x.com/Soala7VA">
<img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white"/>
</a>

</div>

---

<div align="center">

### `> BUILDING SYSTEMS, NOT JUST SOFTWARE.`

<br>

**If it can be done i'll do it.**

<br>

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=18&duration=2500&pause=800&color=00BFFF&center=true&vCenter=true&width=800&lines=Software+%E2%86%92+Systems+%E2%86%92+Hardware;AI+%E2%86%92+Embedded+%E2%86%92+Robotics;Learning+%E2%86%92+Building+%E2%86%92+Understanding;The+journey+is+just+beginning."/>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:001F54,50:005CFF,100:00BFFF&height=140&section=footer&animation=fadeIn"/>

</div>
