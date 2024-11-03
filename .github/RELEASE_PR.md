## Release summary

Version number: [e.g. 1.0.1]

## Release details

Describe in short the main changes with the new release.

## Checklist

_Put an `x` in the boxes that apply._

- [ ] I have read the [CONTRIBUTING](../master/CONTRIBUTING.rst) doc
- [ ] I am making a pull request against the `master` branch (left side), from `develop`
- [ ] I've updated the dependencies versions in `Pipfile` to the latest, wherever is possible.
- [ ] Lint and unit tests pass locally
- [ ] I built the documentation and updated it with the latest changes
- [ ] I've added an item in `HISTORY.md` for this release
- [ ] I bumped the version number in the `__version__.py` file.
- [ ] I published the latest version on TestPyPI and checked that the following command work:
       ```pip install fond4ltlf==<version-number> --index-url https://testpypi.org/simple --force --no-cache-dir --no-deps```
- [ ] After merging the PR, I'll publish the build also on PyPI. Then, I'll make sure the following
      command will work:
      ```pip install fond4ltlf==<version_number> --force --no-cache-dir --no-deps```  


## Further comments

Write here any other comment about the release, if any.
