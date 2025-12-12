## 1. Prerequisites

### Install Python

* Required version: **Python 3.11**
* Verify installation:

```ps
$ Set-Alias python C:\pythons\3.11.9\python.exe

$ python --version    # Python 3.11.9
```

### Install Java (required for Spark)

* Install **Java 8 or higher**.
* Verify installation:
> For incompatibility issues, we are going to use **Java 17**\
> *Important* : Java 21 has some issues with writing to buckets, as of now.

```ps
$ java -version   # java 17.0.10 2024-01-16 LTS
                  # Java(TM) SE Runtime Environment (build 17.0.10+11-LTS-240)
                  # Java HotSpot(TM) 64-Bit Server VM (build 17.0.10+11-LTS-240, mixed mode, sharing)
```

### Install Docker

* Download from: [https://www.docker.com/](https://www.docker.com/)
* Verify installation:

```ps
$ docker --version   # Docker version 27.2.0, build 3ab4256
```

### Install Git

```ps
$ git --version      # git version 2.47.0.windows.2
```