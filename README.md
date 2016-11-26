# FuzzLabs

FuzzLabs is a modular fuzzing framework. This repository contains the source code of the new version that is no longer based on Sulley; however, it works in a similar fashion.

The old version (discontinued) can be found at:

  - Source: https://github.com/DCNWS/FuzzLabs
  - Documentation: http://fuzzlabs.dcnws.com

### Why FuzzLabs

Some may ask what is the point having yet another fuzzer when there are such powerful tools as AFL. If you ever asked this question, here you will find the answer: In case you have the source code your best bet probably is AFL. Or, at least you definitely want to give it a go. But, what if there is a product you want to check and you do not have the source code? This mainly happens in two scenarios:

 - You are a security researcher looking into something you have no source code for.
 - You are a company having one or more product without access to the source code and, you want to make sure you are aware of any vulnerabilities.

This is exactly where FuzzLabs and you come in. (more on 'you' later) Just as Sulley, FuzzLabs is a great framework to do black-box fuzz testing.

Basically, the original idea was to take Sulley and modify it to be more flexible and modular so it can be easily extended. Working with the way Sulley required to create the grammars became quite painful when it came to large projects. It was even worse working in virtual teams and see that people come up with their own poorly written code, having serious limitations and not having a common interface to glue things together. Working this way was very time comsuming and far from optimal. I thought it would make sense to have a framework that solves all these problems. Also, if I wanted to fuzz something over Bluetooth or USB, again, it was a nightmare to add support for that in Sulley. FuzzLabs addressed some of these problems and more. The first version of FuzzLabs however used the exact same syntax as Sulley for defining grammars. The new version however uses JSON so that the grammars can be created easier using a web-based interface.

As there were so many things to be changed and so many ideas on what extra featured could be implemented, this new version of FuzzLabs does not depend on Sulley any more. The code was written from scratch, however when it comes to fuzzing, at it's core it basically works in a similar fashion.

What you have to know if you decide to poke around with FuzzLabs is that it is a framework and not a tool that you can just simply execute to get things done. You will have to write code, debug issues, research and reverse engineer protocols, design grammars and so on. The goal of the development is to help you and your team with all of this.

### Components

FuzzLabs is made up of 4 components:

 - Engine - the engine is the service that performs the fuzzing.
 - Web interface - the web interface (once ready) will allow you to manage multiple engines, develop grammars, create fuzzing jobs and support team work.
 - CLI Client - is a small tool for managing engines and debugging.
 - Agents - agents run on the target machine and monitor process status.

### Tech

 - Engine - completely written in Python.
 - Web interface - NodeJS, HTML5 and all kind of web-based stuff.
 - CLI Client - all Python.
 - Agents - mainly C/C++ or whatever it has to be written in.

### Development

This new version of FuzzLabs is currently work in progress but unfortunately this progress is very slow. If you are a developer familiar with JavaScript, AngularJS and NodeJS or, Python, or C/C++ and would like to join the project then you are more than welcome. Have a look at the code: if you can do better (not that difficult I guess)  then it is very likely you will be accepted as a collaborator. :) Otherwise, you can just sumit pull requests, record issues in the issue tracker or just leave a comment. Thank you.

