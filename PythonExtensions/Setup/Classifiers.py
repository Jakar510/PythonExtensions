class Development_Status(object):
    Planning = "Development Status :: 1 - Planning"
    PreAlpha = "Development Status :: 2 - Pre-Alpha"
    Alpha = "Development Status :: 3 - Alpha"
    Beta = "Development Status :: 4 - Beta"
    Production_Stable = "Development Status :: 5 - Production/Stable"
    Mature = "Development Status :: 6 - Mature"
    Inactive = "Development Status :: 7 - Inactive"
class Environment(object):
    class Console(object):
        Console = "Environment :: Console"
        Curses = "Environment :: Console :: Curses"
        Framebuffer = "Environment :: Console :: Framebuffer"
        Newt = "Environment :: Console :: Newt"
        svgalib = "Environment :: Console :: svgalib"



    class GPU(object):
        GPU = "Environment :: GPU"



        class NVIDIA_CUDA(object):
            NVIDIA_CUDA = "Environment :: GPU :: NVIDIA CUDA"
            Zero = "Environment :: GPU :: NVIDIA CUDA :: 9.0"
            One = "Environment :: GPU :: NVIDIA CUDA :: 9.1"
            Two = "Environment :: GPU :: NVIDIA CUDA :: 9.2"
            Three = "Environment :: GPU :: NVIDIA CUDA :: 2.3"
            Five = "Environment :: GPU :: NVIDIA CUDA :: 7.5"



    Handhelds_PDAs = "Environment :: Handhelds/PDA's"



    class MacOS_X(object):
        MacOS_X = "Environment :: MacOS X"
        Aqua = "Environment :: MacOS X :: Aqua"
        Carbon = "Environment :: MacOS X :: Carbon"
        Cocoa = "Environment :: MacOS X :: Cocoa"



    No_Input_Output_Daemon = "Environment :: No Input/Output (Daemon)"
    OpenStack = "Environment :: OpenStack"
    Other_Environment = "Environment :: Other Environment"
    Plugins = "Environment :: Plugins"



    class Web_Environment(object):
        Web_Environment = "Environment :: Web Environment"
        Buffet = "Environment :: Web Environment :: Buffet"
        Mozilla = "Environment :: Web Environment :: Mozilla"
        ToscaWidgets = "Environment :: Web Environment :: ToscaWidgets"



    Win32_MS_Windows = "Environment :: Win32 (MS Windows)"



    class X11_Applications(object):
        X11_Applications = "Environment :: X11 Applications"
        GTK = "Environment :: X11 Applications :: GTK"
        Gnome = "Environment :: X11 Applications :: Gnome"
        KDE = "Environment :: X11 Applications :: KDE"
        Qt = "Environment :: X11 Applications :: Qt"
class Framework(object):
    class AWS_CDK(object):
        AWS_CDK = "Framework :: AWS CDK"
        One = "Framework :: AWS CDK :: 1"



    AiiDA = "Framework :: AiiDA"
    AsyncIO = "Framework :: AsyncIO"
    BEAT = "Framework :: BEAT"
    BFG = "Framework :: BFG"
    Bob = "Framework :: Bob"
    Bottle = "Framework :: Bottle"



    class Buildout(object):
        Buildout = "Framework :: Buildout"
        Extension = "Framework :: Buildout :: Extension"
        Recipe = "Framework :: Buildout :: Recipe"



    class CastleCMS(object):
        CastleCMS = "Framework :: CastleCMS"
        Theme = "Framework :: CastleCMS :: Theme"



    Chandler = "Framework :: Chandler"
    CherryPy = "Framework :: CherryPy"
    CubicWeb = "Framework :: CubicWeb"
    Dash = "Framework :: Dash"



    class Django(object):
        Django = "Framework :: Django"
        Ten = "Framework :: Django :: 1.10"
        Eleven = "Framework :: Django :: 1.11"
        Four = "Framework :: Django :: 1.4"
        Five = "Framework :: Django :: 1.5"
        Six = "Framework :: Django :: 1.6"
        Seven = "Framework :: Django :: 1.7"
        Eight = "Framework :: Django :: 1.8"
        Nine = "Framework :: Django :: 1.9"
        Zero = "Framework :: Django :: 3.0"
        One = "Framework :: Django :: 3.1"
        Two = "Framework :: Django :: 3.2"



    class Django_CMS(object):
        Django_CMS = "Framework :: Django CMS"
        Four = "Framework :: Django CMS :: 3.4"
        Five = "Framework :: Django CMS :: 3.5"
        Six = "Framework :: Django CMS :: 3.6"
        Seven = "Framework :: Django CMS :: 3.7"
        Eight = "Framework :: Django CMS :: 3.8"



    Flake8 = "Framework :: Flake8"
    Flask = "Framework :: Flask"
    Hypothesis = "Framework :: Hypothesis"
    IDLE = "Framework :: IDLE"
    IPython = "Framework :: IPython"
    Jupyter = "Framework :: Jupyter"
    Kedro = "Framework :: Kedro"
    Lektor = "Framework :: Lektor"
    Masonite = "Framework :: Masonite"
    Matplotlib = "Framework :: Matplotlib"
    Nengo = "Framework :: Nengo"
    Odoo = "Framework :: Odoo"
    Opps = "Framework :: Opps"
    Paste = "Framework :: Paste"



    class Pelican(object):
        Pelican = "Framework :: Pelican"
        Plugins = "Framework :: Pelican :: Plugins"
        Themes = "Framework :: Pelican :: Themes"



    class Plone(object):
        Plone = "Framework :: Plone"
        Two = "Framework :: Plone :: 5.2"
        Three = "Framework :: Plone :: 5.3"
        Zero = "Framework :: Plone :: 6.0"
        One = "Framework :: Plone :: 5.1"
        Addon = "Framework :: Plone :: Addon"
        Core = "Framework :: Plone :: Core"
        Theme = "Framework :: Plone :: Theme"



    Pylons = "Framework :: Pylons"
    Pyramid = "Framework :: Pyramid"
    Pytest = "Framework :: Pytest"
    Review_Board = "Framework :: Review Board"



    class Robot_Framework(object):
        Robot_Framework = "Framework :: Robot Framework"
        Library = "Framework :: Robot Framework :: Library"
        Tool = "Framework :: Robot Framework :: Tool"



    Scrapy = "Framework :: Scrapy"
    Setuptools_Plugin = "Framework :: Setuptools Plugin"



    class Sphinx(object):
        Sphinx = "Framework :: Sphinx"
        Extension = "Framework :: Sphinx :: Extension"
        Theme = "Framework :: Sphinx :: Theme"



    Trac = "Framework :: Trac"
    Trio = "Framework :: Trio"
    Tryton = "Framework :: Tryton"



    class TurboGears(object):
        TurboGears = "Framework :: TurboGears"
        Applications = "Framework :: TurboGears :: Applications"
        Widgets = "Framework :: TurboGears :: Widgets"



    Twisted = "Framework :: Twisted"



    class Wagtail(object):
        Wagtail = "Framework :: Wagtail"
        One = "Framework :: Wagtail :: 1"
        Two = "Framework :: Wagtail :: 2"



    ZODB = "Framework :: ZODB"



    class Zope(object):
        Zope = "Framework :: Zope"
        Two = "Framework :: Zope :: 2"
        Three = "Framework :: Zope :: 3"
        Four = "Framework :: Zope :: 4"
        Five = "Framework :: Zope :: 5"



    Zope2 = "Framework :: Zope2"
    Zope3 = "Framework :: Zope3"
    napari = "Framework :: napari"
    tox = "Framework :: tox"
class Intended_Audience(object):
    Customer_Service = "Intended Audience :: Customer Service"
    Developers = "Intended Audience :: Developers"
    Education = "Intended Audience :: Education"
    End_Users_Desktop = "Intended Audience :: End Users/Desktop"
    Financial_and_Insurance_Industry = "Intended Audience :: Financial and Insurance Industry"
    Healthcare_Industry = "Intended Audience :: Healthcare Industry"
    Information_Technology = "Intended Audience :: Information Technology"
    Legal_Industry = "Intended Audience :: Legal Industry"
    Manufacturing = "Intended Audience :: Manufacturing"
    Other_Audience = "Intended Audience :: Other Audience"
    Religion = "Intended Audience :: Religion"
    Science_Research = "Intended Audience :: Science/Research"
    System_Administrators = "Intended Audience :: System Administrators"
    Telecommunications_Industry = "Intended Audience :: Telecommunications Industry"
class License(object):
    Aladdin_Free_Public_License_AFPL = "License :: Aladdin Free Public License (AFPL)"
    CC0_1_0_Universal_CC0_1_0_Public_Domain_Dedication = "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    CeCILLB_Free_Software_License_Agreement_CECILLB = "License :: CeCILL-B Free Software License Agreement (CECILL-B)"
    CeCILLC_Free_Software_License_Agreement_CECILLC = "License :: CeCILL-C Free Software License Agreement (CECILL-C)"
    DFSG_approved = "License :: DFSG approved"
    Eiffel_Forum_License_EFL = "License :: Eiffel Forum License (EFL)"
    Free_For_Educational_Use = "License :: Free For Educational Use"
    Free_For_Home_Use = "License :: Free For Home Use"
    Free_To_Use_But_Restricted = "License :: Free To Use But Restricted"
    Free_for_noncommercial_use = "License :: Free for non-commercial use"
    Freely_Distributable = "License :: Freely Distributable"
    Freeware = "License :: Freeware"
    GUST_Font_License_1_0 = "License :: GUST Font License 1.0"
    GUST_Font_License_20060930 = "License :: GUST Font License 2006-09-30"
    Netscape_Public_License_NPL = "License :: Netscape Public License (NPL)"
    Nokia_Open_Source_License_NOKOS = "License :: Nokia Open Source License (NOKOS)"



    class OSI_Approved(object):
        OSI_Approved = "License :: OSI Approved"
        Academic_Free_License_AFL = "License :: OSI Approved :: Academic Free License (AFL)"
        Apache_Software_License = "License :: OSI Approved :: Apache Software License"
        Apple_Public_Source_License = "License :: OSI Approved :: Apple Public Source License"
        Artistic_License = "License :: OSI Approved :: Artistic License"
        Attribution_Assurance_License = "License :: OSI Approved :: Attribution Assurance License"
        BSD_License = "License :: OSI Approved :: BSD License"
        Boost_Software_License_1_0_BSL1_0 = "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)"
        CEA_CNRS_Inria_Logiciel_Libre_License_version_2_1_CeCILL2_1 = "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
        Common_Development_and_Distribution_License_1_0_CDDL1_0 = "License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)"
        Common_Public_License = "License :: OSI Approved :: Common Public License"
        Eclipse_Public_License_1_0_EPL1_0 = "License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)"
        Eclipse_Public_License_2_0_EPL2_0 = "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)"
        Eiffel_Forum_License = "License :: OSI Approved :: Eiffel Forum License"
        European_Union_Public_Licence_1_0_EUPL_1_0 = "License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)"
        European_Union_Public_Licence_1_1_EUPL_1_1 = "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)"
        European_Union_Public_Licence_1_2_EUPL_1_2 = "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)"
        GNU_Affero_General_Public_License_v3 = "License :: OSI Approved :: GNU Affero General Public License v3"
        GNU_Affero_General_Public_License_v3_or_later_AGPLv3_plus = "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
        GNU_Free_Documentation_License_FDL = "License :: OSI Approved :: GNU Free Documentation License (FDL)"
        GNU_General_Public_License_GPL = "License :: OSI Approved :: GNU General Public License (GPL)"
        GNU_General_Public_License_v2_GPLv2 = "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
        GNU_General_Public_License_v2_or_later_GPLv2_plus = "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)"
        GNU_General_Public_License_v3_GPLv3 = "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        GNU_General_Public_License_v3_or_later_GPLv3_plus = "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
        GNU_Lesser_General_Public_License_v2_LGPLv2 = "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)"
        GNU_Lesser_General_Public_License_v2_or_later_LGPLv2_plus = "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
        GNU_Lesser_General_Public_License_v3_LGPLv3 = "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
        GNU_Lesser_General_Public_License_v3_or_later_LGPLv3_plus = "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
        GNU_Library_or_Lesser_General_Public_License_LGPL = "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)"
        Historical_Permission_Notice_and_Disclaimer_HPND = "License :: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)"
        IBM_Public_License = "License :: OSI Approved :: IBM Public License"
        ISC_License_ISCL = "License :: OSI Approved :: ISC License (ISCL)"
        Intel_Open_Source_License = "License :: OSI Approved :: Intel Open Source License"
        Jabber_Open_Source_License = "License :: OSI Approved :: Jabber Open Source License"
        MIT_License = "License :: OSI Approved :: MIT License"
        MITRE_Collaborative_Virtual_Workspace_License_CVW = "License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)"
        MirOS_License_MirOS = "License :: OSI Approved :: MirOS License (MirOS)"
        Motosoto_License = "License :: OSI Approved :: Motosoto License"
        Mozilla_Public_License_1_0_MPL = "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)"
        Mozilla_Public_License_1_1_MPL_1_1 = "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)"
        Mozilla_Public_License_2_0_MPL_2_0 = "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"
        Nethack_General_Public_License = "License :: OSI Approved :: Nethack General Public License"
        Nokia_Open_Source_License = "License :: OSI Approved :: Nokia Open Source License"
        Open_Group_Test_Suite_License = "License :: OSI Approved :: Open Group Test Suite License"
        Open_Software_License_3_0_OSL3_0 = "License :: OSI Approved :: Open Software License 3.0 (OSL-3.0)"
        PostgreSQL_License = "License :: OSI Approved :: PostgreSQL License"
        Python_License_CNRI_Python_License = "License :: OSI Approved :: Python License (CNRI Python License)"
        Python_Software_Foundation_License = "License :: OSI Approved :: Python Software Foundation License"
        Qt_Public_License_QPL = "License :: OSI Approved :: Qt Public License (QPL)"
        Ricoh_Source_Code_Public_License = "License :: OSI Approved :: Ricoh Source Code Public License"
        SIL_Open_Font_License_1_1_OFL1_1 = "License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)"
        Sleepycat_License = "License :: OSI Approved :: Sleepycat License"
        Sun_Industry_Standards_Source_License_SISSL = "License :: OSI Approved :: Sun Industry Standards Source License (SISSL)"
        Sun_Public_License = "License :: OSI Approved :: Sun Public License"
        The_Unlicense_Unlicense = "License :: OSI Approved :: The Unlicense (Unlicense)"
        Universal_Permissive_License_UPL = "License :: OSI Approved :: Universal Permissive License (UPL)"
        University_of_Illinois_NCSA_Open_Source_License = "License :: OSI Approved :: University of Illinois/NCSA Open Source License"
        Vovida_Software_License_1_0 = "License :: OSI Approved :: Vovida Software License 1.0"
        W3C_License = "License :: OSI Approved :: W3C License"
        X_Net_License = "License :: OSI Approved :: X.Net License"
        Zope_Public_License = "License :: OSI Approved :: Zope Public License"
        zlib_libpng_License = "License :: OSI Approved :: zlib/libpng License"



    Other_Proprietary_License = "License :: Other/Proprietary License"
    Public_Domain = "License :: Public Domain"
    Repoze_Public_License = "License :: Repoze Public License"
class Natural_Language(object):
    Afrikaans = "Natural Language :: Afrikaans"
    Arabic = "Natural Language :: Arabic"
    Basque = "Natural Language :: Basque"
    Bengali = "Natural Language :: Bengali"
    Bosnian = "Natural Language :: Bosnian"
    Bulgarian = "Natural Language :: Bulgarian"
    Cantonese = "Natural Language :: Cantonese"
    Catalan = "Natural Language :: Catalan"
    Chinese_Simplified = "Natural Language :: Chinese (Simplified)"
    Chinese_Traditional = "Natural Language :: Chinese (Traditional)"
    Croatian = "Natural Language :: Croatian"
    Czech = "Natural Language :: Czech"
    Danish = "Natural Language :: Danish"
    Dutch = "Natural Language :: Dutch"
    English = "Natural Language :: English"
    Esperanto = "Natural Language :: Esperanto"
    Finnish = "Natural Language :: Finnish"
    French = "Natural Language :: French"
    Galician = "Natural Language :: Galician"
    German = "Natural Language :: German"
    Greek = "Natural Language :: Greek"
    Hebrew = "Natural Language :: Hebrew"
    Hindi = "Natural Language :: Hindi"
    Hungarian = "Natural Language :: Hungarian"
    Icelandic = "Natural Language :: Icelandic"
    Indonesian = "Natural Language :: Indonesian"
    Irish = "Natural Language :: Irish"
    Italian = "Natural Language :: Italian"
    Japanese = "Natural Language :: Japanese"
    Javanese = "Natural Language :: Javanese"
    Korean = "Natural Language :: Korean"
    Latin = "Natural Language :: Latin"
    Latvian = "Natural Language :: Latvian"
    Lithuanian = "Natural Language :: Lithuanian"
    Macedonian = "Natural Language :: Macedonian"
    Malay = "Natural Language :: Malay"
    Marathi = "Natural Language :: Marathi"
    Nepali = "Natural Language :: Nepali"
    Norwegian = "Natural Language :: Norwegian"
    Panjabi = "Natural Language :: Panjabi"
    Persian = "Natural Language :: Persian"
    Polish = "Natural Language :: Polish"
    Portuguese = "Natural Language :: Portuguese"
    Portuguese_Brazilian = "Natural Language :: Portuguese (Brazilian)"
    Romanian = "Natural Language :: Romanian"
    Russian = "Natural Language :: Russian"
    Serbian = "Natural Language :: Serbian"
    Slovak = "Natural Language :: Slovak"
    Slovenian = "Natural Language :: Slovenian"
    Spanish = "Natural Language :: Spanish"
    Swedish = "Natural Language :: Swedish"
    Tamil = "Natural Language :: Tamil"
    Telugu = "Natural Language :: Telugu"
    Thai = "Natural Language :: Thai"
    Tibetan = "Natural Language :: Tibetan"
    Turkish = "Natural Language :: Turkish"
    Ukrainian = "Natural Language :: Ukrainian"
    Urdu = "Natural Language :: Urdu"
    Vietnamese = "Natural Language :: Vietnamese"
class Operating_System(object):
    Android = "Operating System :: Android"
    BeOS = "Operating System :: BeOS"



    class MacOS(object):
        MacOS = "Operating System :: MacOS"
        MacOS_9 = "Operating System :: MacOS :: MacOS 9"
        MacOS_X = "Operating System :: MacOS :: MacOS X"



    class Microsoft(object):
        Microsoft = "Operating System :: Microsoft"
        MSDOS = "Operating System :: Microsoft :: MS-DOS"



        class Windows(object):
            Windows = "Operating System :: Microsoft :: Windows"
            Windows_10 = "Operating System :: Microsoft :: Windows :: Windows 10"
            Windows_3_1_or_Earlier = "Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier"
            Windows_7 = "Operating System :: Microsoft :: Windows :: Windows 7"
            Windows_8 = "Operating System :: Microsoft :: Windows :: Windows 8"
            Windows_8_1 = "Operating System :: Microsoft :: Windows :: Windows 8.1"
            Windows_95_98_2000 = "Operating System :: Microsoft :: Windows :: Windows 95/98/2000"
            Windows_CE = "Operating System :: Microsoft :: Windows :: Windows CE"
            Windows_NT_2000 = "Operating System :: Microsoft :: Windows :: Windows NT/2000"
            Windows_Server_2003 = "Operating System :: Microsoft :: Windows :: Windows Server 2003"
            Windows_Server_2008 = "Operating System :: Microsoft :: Windows :: Windows Server 2008"
            Windows_Vista = "Operating System :: Microsoft :: Windows :: Windows Vista"
            Windows_XP = "Operating System :: Microsoft :: Windows :: Windows XP"



    OS_Independent = "Operating System :: OS Independent"
    OS_2 = "Operating System :: OS/2"
    Other_OS = "Operating System :: Other OS"
    PDA_Systems = "Operating System :: PDA Systems"



    class POSIX(object):
        POSIX = "Operating System :: POSIX"
        AIX = "Operating System :: POSIX :: AIX"



        class BSD(object):
            BSD = "Operating System :: POSIX :: BSD"
            BSD_OS = "Operating System :: POSIX :: BSD :: BSD/OS"
            FreeBSD = "Operating System :: POSIX :: BSD :: FreeBSD"
            NetBSD = "Operating System :: POSIX :: BSD :: NetBSD"
            OpenBSD = "Operating System :: POSIX :: BSD :: OpenBSD"



        GNU_Hurd = "Operating System :: POSIX :: GNU Hurd"
        HPUX = "Operating System :: POSIX :: HP-UX"
        IRIX = "Operating System :: POSIX :: IRIX"
        Linux = "Operating System :: POSIX :: Linux"
        Other = "Operating System :: POSIX :: Other"
        SCO = "Operating System :: POSIX :: SCO"
        SunOS_Solaris = "Operating System :: POSIX :: SunOS/Solaris"



    PalmOS = "Operating System :: PalmOS"
    RISC_OS = "Operating System :: RISC OS"
    Unix = "Operating System :: Unix"
    iOS = "Operating System :: iOS"
class Programming_Language(object):
    APL = "Programming Language :: APL"
    ASP = "Programming Language :: ASP"
    Ada = "Programming Language :: Ada"
    Assembly = "Programming Language :: Assembly"
    Awk = "Programming Language :: Awk"
    Basic = "Programming Language :: Basic"
    C = "Programming Language :: C"
    C_sharp = "Programming Language :: C#"
    C_plus_plus = "Programming Language :: C++"
    Cold_Fusion = "Programming Language :: Cold Fusion"
    Cython = "Programming Language :: Cython"
    Delphi_Kylix = "Programming Language :: Delphi/Kylix"
    Dylan = "Programming Language :: Dylan"
    Eiffel = "Programming Language :: Eiffel"
    EmacsLisp = "Programming Language :: Emacs-Lisp"
    Erlang = "Programming Language :: Erlang"
    Euler = "Programming Language :: Euler"
    Euphoria = "Programming Language :: Euphoria"
    F_sharp = "Programming Language :: F#"
    Forth = "Programming Language :: Forth"
    Fortran = "Programming Language :: Fortran"
    Haskell = "Programming Language :: Haskell"
    Java = "Programming Language :: Java"
    JavaScript = "Programming Language :: JavaScript"
    Kotlin = "Programming Language :: Kotlin"
    Lisp = "Programming Language :: Lisp"
    Logo = "Programming Language :: Logo"
    ML = "Programming Language :: ML"
    Modula = "Programming Language :: Modula"
    OCaml = "Programming Language :: OCaml"
    Object_Pascal = "Programming Language :: Object Pascal"
    Objective_C = "Programming Language :: Objective C"
    Other = "Programming Language :: Other"
    Other_Scripting_Engines = "Programming Language :: Other Scripting Engines"
    PHP = "Programming Language :: PHP"
    PL_SQL = "Programming Language :: PL/SQL"
    PROGRESS = "Programming Language :: PROGRESS"
    Pascal = "Programming Language :: Pascal"
    Perl = "Programming Language :: Perl"
    Pike = "Programming Language :: Pike"
    Pliant = "Programming Language :: Pliant"
    Prolog = "Programming Language :: Prolog"



    class Python(object):
        Python = "Programming Language :: Python"



        class Two(object):
            Two = "Programming Language :: Python :: 3.2"
            Only = "Programming Language :: Python :: 2 :: Only"



        class Three(object):
            Three = "Programming Language :: Python :: 3.3"
            Only = "Programming Language :: Python :: 3 :: Only"



        Four = "Programming Language :: Python :: 3.4"
        Five = "Programming Language :: Python :: 3.5"
        Six = "Programming Language :: Python :: 3.6"
        Seven = "Programming Language :: Python :: 3.7"
        Zero = "Programming Language :: Python :: 3.0"
        One = "Programming Language :: Python :: 3.1"
        Ten = "Programming Language :: Python :: 3.10"
        Eight = "Programming Language :: Python :: 3.8"
        Nine = "Programming Language :: Python :: 3.9"



        class Implementation(object):
            Implementation = "Programming Language :: Python :: Implementation"
            CPython = "Programming Language :: Python :: Implementation :: CPython"
            IronPython = "Programming Language :: Python :: Implementation :: IronPython"
            Jython = "Programming Language :: Python :: Implementation :: Jython"
            MicroPython = "Programming Language :: Python :: Implementation :: MicroPython"
            PyPy = "Programming Language :: Python :: Implementation :: PyPy"
            Stackless = "Programming Language :: Python :: Implementation :: Stackless"



    R = "Programming Language :: R"
    REBOL = "Programming Language :: REBOL"
    Rexx = "Programming Language :: Rexx"
    Ruby = "Programming Language :: Ruby"
    Rust = "Programming Language :: Rust"
    SQL = "Programming Language :: SQL"
    Scheme = "Programming Language :: Scheme"
    Simula = "Programming Language :: Simula"
    Smalltalk = "Programming Language :: Smalltalk"
    Tcl = "Programming Language :: Tcl"
    Unix_Shell = "Programming Language :: Unix Shell"
    Visual_Basic = "Programming Language :: Visual Basic"
    XBasic = "Programming Language :: XBasic"
    YACC = "Programming Language :: YACC"
    Zope = "Programming Language :: Zope"
class Topic(object):
    Adaptive_Technologies = "Topic :: Adaptive Technologies"
    Artistic_Software = "Topic :: Artistic Software"



    class Communications(object):
        Communications = "Topic :: Communications"
        BBS = "Topic :: Communications :: BBS"



        class Chat(object):
            Chat = "Topic :: Communications :: Chat"
            ICQ = "Topic :: Communications :: Chat :: ICQ"
            Internet_Relay_Chat = "Topic :: Communications :: Chat :: Internet Relay Chat"
            Unix_Talk = "Topic :: Communications :: Chat :: Unix Talk"



        Conferencing = "Topic :: Communications :: Conferencing"



        class Email(object):
            Email = "Topic :: Communications :: Email"
            Address_Book = "Topic :: Communications :: Email :: Address Book"
            Email_Clients_MUA = "Topic :: Communications :: Email :: Email Clients (MUA)"
            Filters = "Topic :: Communications :: Email :: Filters"
            Mail_Transport_Agents = "Topic :: Communications :: Email :: Mail Transport Agents"
            Mailing_List_Servers = "Topic :: Communications :: Email :: Mailing List Servers"



            class PostOffice(object):
                PostOffice = "Topic :: Communications :: Email :: Post-Office"
                IMAP = "Topic :: Communications :: Email :: Post-Office :: IMAP"
                POP3 = "Topic :: Communications :: Email :: Post-Office :: POP3"



        FIDO = "Topic :: Communications :: FIDO"
        Fax = "Topic :: Communications :: Fax"



        class File_Sharing(object):
            File_Sharing = "Topic :: Communications :: FileIO Sharing"
            Gnutella = "Topic :: Communications :: FileIO Sharing :: Gnutella"
            Napster = "Topic :: Communications :: FileIO Sharing :: Napster"



        Ham_Radio = "Topic :: Communications :: Ham Radio"
        Internet_Phone = "Topic :: Communications :: Internet Phone"
        Telephony = "Topic :: Communications :: Telephony"
        Usenet_News = "Topic :: Communications :: Usenet News"



    class Database(object):
        Database = "Topic :: Database"
        Database_Engines_Servers = "Topic :: Database :: Database Engines/Servers"
        FrontEnds = "Topic :: Database :: Front-Ends"



    class Desktop_Environment(object):
        Desktop_Environment = "Topic :: Desktop Environment"
        File_Managers = "Topic :: Desktop Environment :: FileIO Managers"
        GNUstep = "Topic :: Desktop Environment :: GNUstep"
        Gnome = "Topic :: Desktop Environment :: Gnome"



        class K_Desktop_Environment_KDE(object):
            K_Desktop_Environment_KDE = "Topic :: Desktop Environment :: K Desktop Environment (KDE)"
            Themes = "Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes"



        class PicoGUI(object):
            PicoGUI = "Topic :: Desktop Environment :: PicoGUI"
            Applications = "Topic :: Desktop Environment :: PicoGUI :: Applications"
            Themes = "Topic :: Desktop Environment :: PicoGUI :: Themes"



        Screen_Savers = "Topic :: Desktop Environment :: Screen Savers"



        class Window_Managers(object):
            Window_Managers = "Topic :: Desktop Environment :: Window Managers"



            class Afterstep(object):
                Afterstep = "Topic :: Desktop Environment :: Window Managers :: Afterstep"
                Themes = "Topic :: Desktop Environment :: Window Managers :: Afterstep :: Themes"



            Applets = "Topic :: Desktop Environment :: Window Managers :: Applets"



            class Blackbox(object):
                Blackbox = "Topic :: Desktop Environment :: Window Managers :: Blackbox"
                Themes = "Topic :: Desktop Environment :: Window Managers :: Blackbox :: Themes"



            class CTWM(object):
                CTWM = "Topic :: Desktop Environment :: Window Managers :: CTWM"
                Themes = "Topic :: Desktop Environment :: Window Managers :: CTWM :: Themes"



            class Enlightenment(object):
                Enlightenment = "Topic :: Desktop Environment :: Window Managers :: Enlightenment"
                Epplets = "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Epplets"
                Themes_DR15 = "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR15"
                Themes_DR16 = "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR16"
                Themes_DR17 = "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR17"



            class FVWM(object):
                FVWM = "Topic :: Desktop Environment :: Window Managers :: FVWM"
                Themes = "Topic :: Desktop Environment :: Window Managers :: FVWM :: Themes"



            class Fluxbox(object):
                Fluxbox = "Topic :: Desktop Environment :: Window Managers :: Fluxbox"
                Themes = "Topic :: Desktop Environment :: Window Managers :: Fluxbox :: Themes"



            class IceWM(object):
                IceWM = "Topic :: Desktop Environment :: Window Managers :: IceWM"
                Themes = "Topic :: Desktop Environment :: Window Managers :: IceWM :: Themes"



            class MetaCity(object):
                MetaCity = "Topic :: Desktop Environment :: Window Managers :: MetaCity"
                Themes = "Topic :: Desktop Environment :: Window Managers :: MetaCity :: Themes"



            class Oroborus(object):
                Oroborus = "Topic :: Desktop Environment :: Window Managers :: Oroborus"
                Themes = "Topic :: Desktop Environment :: Window Managers :: Oroborus :: Themes"



            class Sawfish(object):
                Sawfish = "Topic :: Desktop Environment :: Window Managers :: Sawfish"
                Themes_0_30 = "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes 0.30"
                Themes_pre0_30 = "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes pre-0.30"



            class Waimea(object):
                Waimea = "Topic :: Desktop Environment :: Window Managers :: Waimea"
                Themes = "Topic :: Desktop Environment :: Window Managers :: Waimea :: Themes"



            class Window_Maker(object):
                Window_Maker = "Topic :: Desktop Environment :: Window Managers :: Window Maker"
                Applets = "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Applets"
                Themes = "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Themes"



            class XFCE(object):
                XFCE = "Topic :: Desktop Environment :: Window Managers :: XFCE"
                Themes = "Topic :: Desktop Environment :: Window Managers :: XFCE :: Themes"



    class Documentation(object):
        Documentation = "Topic :: Documentation"
        Sphinx = "Topic :: Documentation :: Sphinx"



    class Education(object):
        Education = "Topic :: Education"
        Computer_Aided_Instruction_CAI = "Topic :: Education :: Computer Aided Instruction (CAI)"
        Testing = "Topic :: Education :: Testing"



    class Games_Entertainment(object):
        Games_Entertainment = "Topic :: Games/Entertainment"
        Arcade = "Topic :: Games/Entertainment :: Arcade"
        Board_Games = "Topic :: Games/Entertainment :: Board Games"
        First_Person_Shooters = "Topic :: Games/Entertainment :: First Person Shooters"
        Fortune_Cookies = "Topic :: Games/Entertainment :: Fortune Cookies"
        MultiUser_Dungeons_MUD = "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)"
        Puzzle_Games = "Topic :: Games/Entertainment :: Puzzle Games"
        Real_Time_Strategy = "Topic :: Games/Entertainment :: Real Time Strategy"
        RolePlaying = "Topic :: Games/Entertainment :: Role-Playing"
        SideScrolling_Arcade_Games = "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games"
        Simulation = "Topic :: Games/Entertainment :: Simulation"
        Turn_Based_Strategy = "Topic :: Games/Entertainment :: Turn Based Strategy"



    Home_Automation = "Topic :: Home Automation"



    class Internet(object):
        Internet = "Topic :: Internet"
        File_Transfer_Protocol_FTP = "Topic :: Internet :: FileIO Transfer Protocol (FTP)"
        Finger = "Topic :: Internet :: Finger"
        Log_Analysis = "Topic :: Internet :: Log Analysis"
        Name_Service_DNS = "Topic :: Internet :: Name Service (DNS)"
        Proxy_Servers = "Topic :: Internet :: Proxy Servers"
        WAP = "Topic :: Internet :: WAP"



        class WWW_HTTP(object):
            WWW_HTTP = "Topic :: Internet :: WWW/HTTP"
            Browsers = "Topic :: Internet :: WWW/HTTP :: Browsers"



            class Dynamic_Content(object):
                Dynamic_Content = "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
                CGI_Tools_Libraries = "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries"
                Content_Management_System = "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System"
                Message_Boards = "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards"
                News_Diary = "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary"
                Page_Counters = "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters"
                Wiki = "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki"



            HTTP_Servers = "Topic :: Internet :: WWW/HTTP :: HTTP Servers"
            Indexing_Search = "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
            Session = "Topic :: Internet :: WWW/HTTP :: Session"



            class Site_Management(object):
                Site_Management = "Topic :: Internet :: WWW/HTTP :: Site Management"
                Link_Checking = "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking"



            class WSGI(object):
                WSGI = "Topic :: Internet :: WWW/HTTP :: WSGI"
                Application = "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
                Middleware = "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware"
                Server = "Topic :: Internet :: WWW/HTTP :: WSGI :: Server"



        XMPP = "Topic :: Internet :: XMPP"
        Z39_50 = "Topic :: Internet :: Z39.50"



    class Multimedia(object):
        Multimedia = "Topic :: Multimedia"



        class Graphics(object):
            Graphics = "Topic :: Multimedia :: Graphics"
            ThreeDimension_Modeling = "Topic :: Multimedia :: Graphics :: 3D Modeling"
            ThreeDimension_Rendering = "Topic :: Multimedia :: Graphics :: 3D Rendering"



            class Capture(object):
                Capture = "Topic :: Multimedia :: Graphics :: Capture"
                Digital_Camera = "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera"
                Scanners = "Topic :: Multimedia :: Graphics :: Capture :: Scanners"
                Screen_Capture = "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture"



            class Editors(object):
                Editors = "Topic :: Multimedia :: Graphics :: Editors"
                RasterBased = "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based"
                VectorBased = "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based"



            Graphics_Conversion = "Topic :: Multimedia :: Graphics :: Graphics Conversion"
            Presentation = "Topic :: Multimedia :: Graphics :: Presentation"
            Viewers = "Topic :: Multimedia :: Graphics :: Viewers"



        class Sound_Audio(object):
            Sound_Audio = "Topic :: Multimedia :: Sound/Audio"
            Analysis = "Topic :: Multimedia :: Sound/Audio :: Analysis"



            class CD_Audio(object):
                CD_Audio = "Topic :: Multimedia :: Sound/Audio :: CD Audio"
                CD_Playing = "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing"
                CD_Ripping = "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping"
                CD_Writing = "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing"



            Capture_Recording = "Topic :: Multimedia :: Sound/Audio :: Capture/Recording"
            Conversion = "Topic :: Multimedia :: Sound/Audio :: Conversion"
            Editors = "Topic :: Multimedia :: Sound/Audio :: Editors"
            MIDI = "Topic :: Multimedia :: Sound/Audio :: MIDI"
            Mixers = "Topic :: Multimedia :: Sound/Audio :: Mixers"



            class Players(object):
                Players = "Topic :: Multimedia :: Sound/Audio :: Players"
                MP3 = "Topic :: Multimedia :: Sound/Audio :: Players :: MP3"



            Sound_Synthesis = "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis"
            Speech = "Topic :: Multimedia :: Sound/Audio :: Speech"



        class Video(object):
            Video = "Topic :: Multimedia :: Video"
            Capture = "Topic :: Multimedia :: Video :: Capture"
            Conversion = "Topic :: Multimedia :: Video :: Conversion"
            Display = "Topic :: Multimedia :: Video :: Display"
            NonLinear_Editor = "Topic :: Multimedia :: Video :: Non-Linear Editor"



    class Office_Business(object):
        Office_Business = "Topic :: Office/Business"



        class Financial(object):
            Financial = "Topic :: Office/Business :: Financial"
            Accounting = "Topic :: Office/Business :: Financial :: Accounting"
            Investment = "Topic :: Office/Business :: Financial :: Investment"
            PointOfSale = "Topic :: Office/Business :: Financial :: Point-Of-Sale"
            Spreadsheet = "Topic :: Office/Business :: Financial :: Spreadsheet"



        Groupware = "Topic :: Office/Business :: Groupware"
        News_Diary = "Topic :: Office/Business :: News/Diary"
        Office_Suites = "Topic :: Office/Business :: Office Suites"
        Scheduling = "Topic :: Office/Business :: Scheduling"



    Other_Nonlisted_Topic = "Topic :: Other/Nonlisted Topic"
    Printing = "Topic :: Printing"
    Religion = "Topic :: Religion"



    class Scientific_Engineering(object):
        Scientific_Engineering = "Topic :: Scientific/Engineering"
        Artificial_Intelligence = "Topic :: Scientific/Engineering :: Artificial Intelligence"
        Artificial_Life = "Topic :: Scientific/Engineering :: Artificial Life"
        Astronomy = "Topic :: Scientific/Engineering :: Astronomy"
        Atmospheric_Science = "Topic :: Scientific/Engineering :: Atmospheric Science"
        BioInformatics = "Topic :: Scientific/Engineering :: Bio-Informatics"
        Chemistry = "Topic :: Scientific/Engineering :: Chemistry"
        Electronic_Design_Automation_EDA = "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
        GIS = "Topic :: Scientific/Engineering :: GIS"
        Human_Machine_Interfaces = "Topic :: Scientific/Engineering :: Human Machine Interfaces"
        Hydrology = "Topic :: Scientific/Engineering :: Hydrology"
        Image_Processing = "Topic :: Scientific/Engineering :: Image Processing"
        Image_Recognition = "Topic :: Scientific/Engineering :: Image Recognition"
        Information_Analysis = "Topic :: Scientific/Engineering :: Information Analysis"
        Interface_Engine_Protocol_Translator = "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator"
        Mathematics = "Topic :: Scientific/Engineering :: Mathematics"
        Medical_Science_Apps_ = "Topic :: Scientific/Engineering :: Medical Science Apps."
        Physics = "Topic :: Scientific/Engineering :: Physics"
        Visualization = "Topic :: Scientific/Engineering :: Visualization"



    class Security(object):
        Security = "Topic :: Security"
        Cryptography = "Topic :: Security :: Cryptography"



    class Sociology(object):
        Sociology = "Topic :: Sociology"
        Genealogy = "Topic :: Sociology :: Genealogy"
        History = "Topic :: Sociology :: History"



    class Software_Development(object):
        Software_Development = "Topic :: Software Development"
        Assemblers = "Topic :: Software Development :: Assemblers"
        Bug_Tracking = "Topic :: Software Development :: Bug Tracking"
        Build_Tools = "Topic :: Software Development :: Build Tools"
        Code_Generators = "Topic :: Software Development :: Code Generators"
        Compilers = "Topic :: Software Development :: Compilers"
        Debuggers = "Topic :: Software Development :: Debuggers"
        Disassemblers = "Topic :: Software Development :: Disassemblers"
        Documentation = "Topic :: Software Development :: Documentation"
        Embedded_Systems = "Topic :: Software Development :: Embedded Systems"
        Internationalization = "Topic :: Software Development :: Internationalization"
        Interpreters = "Topic :: Software Development :: Interpreters"



        class Libraries(object):
            Libraries = "Topic :: Software Development :: Libraries"
            Application_Frameworks = "Topic :: Software Development :: Libraries :: Application Frameworks"
            Java_Libraries = "Topic :: Software Development :: Libraries :: Java Libraries"
            PHP_Classes = "Topic :: Software Development :: Libraries :: PHP Classes"
            Perl_Modules = "Topic :: Software Development :: Libraries :: Perl Modules"
            Pike_Modules = "Topic :: Software Development :: Libraries :: Pike Modules"
            Python_Modules = "Topic :: Software Development :: Libraries :: Python Modules"
            Ruby_Modules = "Topic :: Software Development :: Libraries :: Ruby Modules"
            Tcl_Extensions = "Topic :: Software Development :: Libraries :: Tcl Extensions"
            pygame = "Topic :: Software Development :: Libraries :: pygame"



        Localization = "Topic :: Software Development :: Localization"



        class Object_Brokering(object):
            Object_Brokering = "Topic :: Software Development :: Object Brokering"
            CORBA = "Topic :: Software Development :: Object Brokering :: CORBA"



        Preprocessors = "Topic :: Software Development :: Pre-processors"
        Quality_Assurance = "Topic :: Software Development :: Quality Assurance"



        class Testing(object):
            Testing = "Topic :: Software Development :: Testing"
            Acceptance = "Topic :: Software Development :: Testing :: Acceptance"
            BDD = "Topic :: Software Development :: Testing :: BDD"
            Mocking = "Topic :: Software Development :: Testing :: Mocking"
            Traffic_Generation = "Topic :: Software Development :: Testing :: Traffic Generation"
            Unit = "Topic :: Software Development :: Testing :: Unit"



        User_Interfaces = "Topic :: Software Development :: User Interfaces"



        class Version_Control(object):
            Version_Control = "Topic :: Software Development :: Version Control"
            Bazaar = "Topic :: Software Development :: Version Control :: Bazaar"
            CVS = "Topic :: Software Development :: Version Control :: CVS"
            Git = "Topic :: Software Development :: Version Control :: Git"
            Mercurial = "Topic :: Software Development :: Version Control :: Mercurial"
            RCS = "Topic :: Software Development :: Version Control :: RCS"
            SCCS = "Topic :: Software Development :: Version Control :: SCCS"



        Widget_Sets = "Topic :: Software Development :: Widget Sets"



    class System(object):
        System = "Topic :: System"



        class Archiving(object):
            Archiving = "Topic :: System :: Archiving"
            Backup = "Topic :: System :: Archiving :: Backup"
            Compression = "Topic :: System :: Archiving :: Compression"
            Mirroring = "Topic :: System :: Archiving :: Mirroring"
            Packaging = "Topic :: System :: Archiving :: Packaging"



        Benchmark = "Topic :: System :: Benchmark"



        class Boot(object):
            Boot = "Topic :: System :: Boot"
            Init = "Topic :: System :: Boot :: Init"



        Clustering = "Topic :: System :: Clustering"
        Console_Fonts = "Topic :: System :: Console Fonts"
        Distributed_Computing = "Topic :: System :: Distributed Computing"
        Emulators = "Topic :: System :: Emulators"
        Filesystems = "Topic :: System :: Filesystems"



        class Hardware(object):
            Hardware = "Topic :: System :: Hardware"
            Hardware_Drivers = "Topic :: System :: Hardware :: Hardware Drivers"
            Mainframes = "Topic :: System :: Hardware :: Mainframes"
            Symmetric_Multiprocessing = "Topic :: System :: Hardware :: Symmetric Multi-processing"



        Installation_Setup = "Topic :: System :: Installation/Setup"
        Logging = "Topic :: System :: Logging"
        Monitoring = "Topic :: System :: Monitoring"



        class Networking(object):
            Networking = "Topic :: System :: Networking"
            Firewalls = "Topic :: System :: Networking :: Firewalls"



            class Monitoring(object):
                Monitoring = "Topic :: System :: Networking :: Monitoring"
                Hardware_Watchdog = "Topic :: System :: Networking :: Monitoring :: Hardware Watchdog"



            Time_Synchronization = "Topic :: System :: Networking :: Time Synchronization"



        Operating_System = "Topic :: System :: Operating System"



        class Operating_System_Kernels(object):
            Operating_System_Kernels = "Topic :: System :: Operating System Kernels"
            BSD = "Topic :: System :: Operating System Kernels :: BSD"
            GNU_Hurd = "Topic :: System :: Operating System Kernels :: GNU Hurd"
            Linux = "Topic :: System :: Operating System Kernels :: Linux"



        Power_UPS = "Topic :: System :: Power (UPS)"
        Recovery_Tools = "Topic :: System :: Recovery Tools"
        Shells = "Topic :: System :: Shells"
        Software_Distribution = "Topic :: System :: Software Distribution"
        System_Shells = "Topic :: System :: System Shells"



        class Systems_Administration(object):
            Systems_Administration = "Topic :: System :: Systems Administration"



            class Authentication_Directory(object):
                Authentication_Directory = "Topic :: System :: Systems Administration :: Authentication/Directory"
                LDAP = "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP"
                NIS = "Topic :: System :: Systems Administration :: Authentication/Directory :: NIS"



    class Terminals(object):
        Terminals = "Topic :: Terminals"
        Serial = "Topic :: Terminals :: Serial"
        Telnet = "Topic :: Terminals :: Telnet"
        Terminal_Emulators_X_Terminals = "Topic :: Terminals :: Terminal Emulators/X Terminals"



    class Text_Editors(object):
        Text_Editors = "Topic :: Text Editors"
        Documentation = "Topic :: Text Editors :: Documentation"
        Emacs = "Topic :: Text Editors :: Emacs"
        Integrated_Development_Environments_IDE = "Topic :: Text Editors :: Integrated Development Environments (IDE)"
        Text_Processing = "Topic :: Text Editors :: Text Processing"
        Word_Processors = "Topic :: Text Editors :: Word Processors"



    class Text_Processing(object):
        Text_Processing = "Topic :: Text Processing"
        Filters = "Topic :: Text Processing :: Filters"
        Fonts = "Topic :: Text Processing :: Fonts"
        General = "Topic :: Text Processing :: General"
        Indexing = "Topic :: Text Processing :: Indexing"
        Linguistic = "Topic :: Text Processing :: Linguistic"



        class Markup(object):
            Markup = "Topic :: Text Processing :: Markup"
            HTML = "Topic :: Text Processing :: Markup :: HTML"
            LaTeX = "Topic :: Text Processing :: Markup :: LaTeX"
            Markdown = "Topic :: Text Processing :: Markup :: Markdown"
            SGML = "Topic :: Text Processing :: Markup :: SGML"
            VRML = "Topic :: Text Processing :: Markup :: VRML"
            XML = "Topic :: Text Processing :: Markup :: XML"
            reStructuredText = "Topic :: Text Processing :: Markup :: reStructuredText"



    Utilities = "Topic :: Utilities"
class Typing(object):
    Typed = "Typing :: Typed"
