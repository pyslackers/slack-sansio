============
Contributing
============

First off, thanks for taking the time to contribute!

Contributions are welcome by anybody and everybody. We are not kidding! Looking for help ? Join us on `Slack`_ by requesting an `invite`_.

The rest of this document will be guidelines to contributing to the project. Remember that these are just guidelines, not rules. Use common sense as much as possible.

.. _invite: http://pyslackers.com/
.. _Slack: https://pythondev.slack.com/

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests (if necessary). If you have any questions about how to write tests then ask the community.
2. If the pull request adds functionality update the docs where appropriate.
3. Use a `good commit message`_.

If you have any issues `contributing_git_hygiene`_ might help.

.. _good commit message: https://github.com/spring-projects/spring-framework/blob/30bce7/CONTRIBUTING.md#format-commit-messages


Types of Contributions
----------------------

Report Bugs
^^^^^^^^^^^

The best way to report a bug is to file an `issue <https://github.com/pyslackers/slack-sansio/issues>`_.

Please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs & Features
^^^^^^^^^^^^^^^^^^^

Look through the github issues for bugs or features request.
Anything tagged with "help-wanted" is open to whoever wants to implement it.

Write Documentation
^^^^^^^^^^^^^^^^^^^

Slack-sansio could always use more documentation and examples, whether as part of the
official documentation, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
^^^^^^^^^^^^^^^

The best way to submit feedback is to file an `issue <https://github.com/pyslackers/slack-sansio/issues>`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up ``slack-sansio`` for local development.

1. Fork the ``slack-sansio`` repo on github.
2. Clone your fork locally and add the upstream repository:

   .. code-block:: console

        $ git clone git@github.com:<username>/slack-sansio.git
        $ git remote add upstream https://github.com/pyslackers/slack-sansio.git
        $ cd slack-sansion/

3. Install your local copy into a virtualenv:

   .. code-block:: console

        $ python3 -m venv .env
        $ source .env/bin/activate

4. Install all dependencies

   .. code-block:: console

        $ pip install -e .[dev]

5. Create a branch for local development:

   .. code-block:: console

        $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox:

   .. code-block:: console

        $ tox

7. Commit your changes and push your branch to github:

    .. code-block:: console

        $ git add .
        $ git commit
        $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the github website.

Git Hygiene
-----------

.. _contributing_git_hygiene:

Handling Merge Conflicts
^^^^^^^^^^^^^^^^^^^^^^^^

Occasionally a Pull Request will have Merge Conflicts. **Do not merge master into your branch.** Instead, make sure your :code:`master` branch is up to date:

.. code-block:: console

    $ git checkout master
    $ git pull upstream master
    $ git push origin master

Then rebase your branch on :code:`master`:

.. code-block:: console

    $ git checkout _my-branch_
    $ git rebase master

If there are any conflicts you need to resolve, it will suspend the rebase for you to fix them. Then do:

.. code-block:: console

    $ git add .
    $ git rebase --continue

It will do one round of conflict-checking for each commit in your branch, so keeping your history clean will make rebasing much easier. When the rebase is done, your branch will be up to date with master and ready to issue a PR if you are.
