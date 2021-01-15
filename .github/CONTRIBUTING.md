
# Contributing

Thank you for your interest in contributing to TkinterExtensions! In this document, we'll outline what you need to know about contributing and how to get started.


## Code of Conduct
Please see our [Code of Conduct](CODE_OF_CONDUCT.md).

Third-party contributions are essential for the future development of TkinterExtensions.
We would like to keep it as easy as possible to contribute changes that get things working
on your environment. There are some guidelines that we need contributors to follow
so that we can keep on top of things.


## Getting Started
* Make sure you have a [GitHub account](https://github.com/signup/free).
* Create an Issue for your problem, assuming one does not already exist.
  * Clearly describe the issue including steps to reproduce, stacktrace and environments when it is a bug.
  * We have an [Issue Template](https://github.com/Jakar510/TkinterExtensions/blob/master/.github/ISSUE_TEMPLATE/bug_report.md), you can use some part of it.
  * We have an [Feature Request / Enhancement Template](https://github.com/Jakar510/TkinterExtensions/blob/master/.github/ISSUE_TEMPLATE/feature_request.md), you can use some part of it.
* Fork the repository on GitHub.
* After cloning your repogitory to local, you should set ``git config user.name`` and `` git config user.email your@ema.il`` . Especially you **MUST** set ``user.email`` as same as your GitHub account's e-mail.


## Prerequisite
You will need to complete a Contribution License Agreement before any pull request can be accepted. Review the CLA at https://cla.dotnetfoundation.org/. When you submit a pull request, a CLA assistant bot will confirm you have completed the agreement, or provide you with an opportunity to do so.


## Contributing Code
I follow the same standard as [A Beginner's Guide for Contributing to Xamarin.Forms](https://devblogs.microsoft.com/xamarin/beginners-guide-contributing-xamarin-forms/).


### What to work on
If you're looking for something to work on, please browse [open issues](https://github.com/Jakar510/TkinterExtensions/issues). Any issue that is not already assigned is up for grabs. You can also look for issues tagged <a href="https://github.com/Jakar510/TkinterExtensions/labels/help%20wanted" class="label v-align-text-top labelstyle-159818 linked-labelstyle-159818" data-ga-click="Maintainer label education banner, dismiss, repository_nwo:Jakar510/TkinterExtensions; context:issues; label_name:help wanted; public:true; repo_has_help_wanted_label:true; repo_has_good_first_issue_label:false; shows_go_to_labels:true" data-octo-click="maintainer_label_education" data-octo-dimensions="action:click_label,actor_id:41873,user_id:790012,repository_id:54213490,repository_nwo:xamarin/Xamarin.Forms,context:issues,label_name:help wanted,public:true,repo_has_help_wanted_label:true,repo_has_good_first_issue_label:false,shows_go_to_labels:true" style="background-color: #159818; color: #fff" title="Label: help wanted">help wanted</a>. Before you select an enhancement to work on, see Status of Proposals below. Make sure you're working on something in the Ready For Implementation category!

Follow the style used by the [.NET Foundation](https://github.com/dotnet/corefx/blob/master/Documentation/coding-guidelines/coding-style.md), with a few exceptions:

- We use hard tabs over spaces.

Read and follow our [Pull Request template](PULL_REQUEST_TEMPLATE.md).


### Pull Request Requirements
We use red-green-refactor test driven development. If you're planning to work on a bug fix, please be sure to create a test case in the UI tests suite (or unit tests, if you're working on Core/XAML code) that proves that the behavior is broken and then proves that the behavior was resolved after your changes. If at all possible, the test should be automated. If the test cannot be automated, then it should include manual testing instructions on screen.

Please check the "Allow edits from maintainers" checkbox on your pull request. This allows us to quickly make minor fixes and resolve conflicts for you.


## Proposals/Enhancements/Suggestions
To propose a change or new feature, open an issue using the [Feature request template](https://github.com/Jakar510/TkinterExtensions/blob/master/.github/ISSUE_TEMPLATE/feature_request.md). 
You may also use the [Spec template](https://github.com/Jakar510/TkinterExtensions/blob/master/.github/ISSUE_TEMPLATE/spec.md) if you have an idea of what the API should look like.


### Status of Proposals
Proposals (also called Enhancements or Suggestions) will start out in the [Enhancements project](https://github.com/Jakar510/TkinterExtensions/projects/3) and will be sorted into columns based on their current status.


#### Under consideration
This issue is proposed to the community for further support or ideas. Make your votes, voice your opinions, and help develop a specification that someone can work from. A proposal in this column is likely not ready to be worked on yet.


#### Discussion Required
Similar to "Under consideration", except there are clear reasons or concerns about adding this to the platform. This is not quite a rejected state, but this issue requires a lot of problem solving before it should be worked on.


#### Needs Specification
This idea is accepted to be added to Xamarin.Forms. However, it can't be worked on until it has a clear specification, including API changes, sample use cases, etc. See the [Spec template](https://github.com/xamarin/Xamarin.Forms/issues/new?assignees=&labels=proposal-open%2C+t%2Fenhancement+%E2%9E%95&template=spec.md&title=%5BSpec%5D++) for the type of information that is needed.


#### Needs Design Review
The specification is written for this accepted proposal, and now we need to review it to make sure that it is easy to use, extensible, etc.


#### Ready for Implementation
Issues in this column should be ready to implement; all of the required information should be in the issue at this point. Unless the issue has an assignee already, anyone is welcome to pick something from this column!


#### In Progress
Issues that have a matching PR are automatically removed from this project entirely; however, if someone wants to claim an issue and submit a PR later, the issue should be moved to this column so someone else doesn't start working on it at the same time.


#### External
These issues won't involve code that is in the TkinterExtensions repository, but for one reason or another, it is still tracked here.


#### Closed
Proposals that were closed without being implemented.


## Review Process
All pull requests need to be reviewed and tested for a reasonable amount of time. We do our best to review pull requests in a timely manner, but please be patient! If there are any changes requested, the contributor should make them at their earliest convenience or let the reviewers know that they are unable to make further contributions. If the pull request requires only minor changes, then someone else may pick it up and finish it. We will do our best to make sure that all credit is retained for contributors. 

Once a pull request has two approvals, it will receive an "approved" label. As long as no UI or unit tests are failing, this pull request can be merged at this time.


## Merge Process
Bug fixes should be targeted at the earliest appropriate branch.
- The _current stable branch_ corresponds to the latest stable version available on NuGet.org. This branch will now only accept regressions or fixes that meet a very high bar and low risk.
- The _current prerelease branch_ corresponds to the latest prerelease version available on NuGet.org. This branch will only accept bug fixes without API changes or breaking changes, with the exception of any API that is under an experimental flag.
- _Master_ corresponds to a version that is not yet tagged. This is also the "nightly" branch. This is where anything that doesn't fit into the stable or prerelease branches should be targeted.

Commits will be merged up from stable to prerelease to master branches on a regular basis (typically every Monday and whenever a new release is tagged).


## Making Changes
* Create a topic branch from where you want to base your work.
  * It would be usually from the development branch.
  * To quickly create a topic branch based on development; `git branch
    issue_999 development` then checkout the new branch with `git
    checkout issue_999`. Please avoid working directly on the
    `development` branch.
* Make commits of logical units. **Do not contain unrelated file changes(e.g. code formatting).**
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.

````
Essential commit summary here.

The body paragraph describes the behavior without the patch,
why this is a problem, and how the patch fixes the problem when applied.
````

* Make sure you have added the necessary tests for your changes.
* Run _all_ the tests to assure nothing else was accidentally broken.


### Coding Style
We follow the style used by the [.NET Foundation](https://github.com/dotnet/corefx/blob/master/Documentation/coding-guidelines/coding-style.md), with some exceptions:


## Submitting Changes
* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the AiForms.SettingsView repository.

Make pull request guide line

* Write a summary of the changes in easy-to-understand manner for the title.
* Show some usage or test code for your changes. We storongly recommend to add usage of new feature to the [sample apps](https://github.com/muak/AiForms.SettingsView/tree/development/Sample).
* Reflect the changes on [ReadMe.md](https://github.com/muak/AiForms.SettingsView/blob/development/README.md).
* Include related issue number for the contents. (e.g. ref #199)
* If your changes are work in progress, the title should start with [WIP]. If you worked out, delete the [WIP] and please let us know.
  * If we changed the development before you completed the work, you should resolve conflicts.
  * We accept your [WIP] pull request first, which means issue reservation. But if you became no longer active, we will close it.


# Thanks
This guide is based on [Xamarin.Forms/CONTRIBUTING.en.md](https://github.com/xamarin/Xamarin.Forms/blob/main/.github/CONTRIBUTING.md) and [MMP/CONTRIBUTING.en.md · sn0w75/MMP](https://github.com/sn0w75/MMP/blob/master/CONTRIBUTING.en.md) and [CONTRIBUTING.md · amay077/
Xamarin.Forms.GoogleMaps](https://github.com/amay077/Xamarin.Forms.GoogleMaps/blob/master/CONTRIBUTING.md).

