Changelog
=========

0.2.1 - 2024-07-26
------------------

- Provide a short read timeout as this should be a local service.  This
  prevents a deadlock situation; as Zope 2 isn't async, it is possible
  for a request from here to hit back to Zope and when there isn't
  enough threads available, the BiVeS server will wait until timeout,
  which in turn will cause requests to wait until its timeout, which
  further holds up the thread.

0.2.0 - 2020-01-17
------------------

- Create new request session by default

0.1.1 - 2017-04-11
------------------

- Updated CDN locations for MathJax.

0.1 - 2016-03-08
----------------

- Initial release of the BiVeS addon for PMR2, covering the rendering of
  math equations and showing difference between models.
