# Documentation

The documentation is written in Markdown and is available under the `docs` folder. The documentation is built using [DocFx](https://dotnet.github.io/docfx/).

## Local Development

### Prerequisites

- [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/) (only for Windows users)
- [Powershell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell) (recommended for Windows users)
- [.NET SDK](https://dotnet.microsoft.com/download) (required for DocFx, LTS version recommended)
- [DocFx](https://dotnet.github.io/docfx/)
- [Node.js](https://nodejs.org/) (optional for automatic documentation generation)


### Installing Prerequisites

WinGet should already be installed directly on Windows 10 1709 or higher. If not, you can get it through the Microsoft Store or by following the instructions on the [official documentation](https://learn.microsoft.com/en-us/windows/package-manager/winget/).

With WinGet installed, you can install the remaining prerequisites by running the following commands on Powershell for Windows:

```powershell
# install Powershell 7.x
winget install --id Microsoft.Powershell --source winget
# install .NET SDK 8 LTS version
winget install -e --id Microsoft.DotNet.SDK.8
# install Node.js (optional, only required for automatic documentation generation)
winget install -e --id OpenJS.Nodejs.LTS
```

### Installing DocFx
Now open a new `Powershell 7` window and run the following commands:

```powershell
# verify .NET SDK installation
dotnet --version

# install DocFx
dotnet tool install -g docfx
```

### Cloning the Repository

You can clone the repository using the following command:

```bash
git clone --recurse-submodules git@github.com:fchampalimaud/cf.bonsai.git
cd cf.bonsai
```

If for some reason you forgot to clone the submodules, you can run the following command to get them:

```bash
git submodule update --init --recursive
```

### First setup

To build the documentation, you need to install the dependencies. You can do this by running the following commands at the `docs` folder:

```bash
dotnet tool restore

# if you have NodeJS installed, you need to install the NodeJS dependencies
npm install
```

Now we need to setup Bonsai locally. You can do this by running the following command at the `bonsai` folder in a Powershell window:

```powershell
.\Setup.ps1
```

### Generating SVG images from Bonsai workflows

To generate the SVG images from the Bonsai workflows and generate the documentation, you need to run the following command at the `docs` folder:

```powershell
.\build.ps1
```

This is required to be done every time you add a new workflow to the `workflows` folder.

### Building the Documentation

To generate the documentation you need to run the following command while at the `docs` folder.

```powershell
docfx --serve

# or if you have Node installed (it will automatically update the documentation on each .md and .yml file change)
npm run docfx
```

The documentation will be available at [http://localhost:8080](http://localhost:8080).

If you want to update the documentation, you will need to stop the server and run `docfx --serve` again.