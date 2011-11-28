%define	__php_provides	/usr/lib/rpm/php.prov
# define 'php_req_new' in ~/.rpmmacros to use php version of req finder
%define	__php_requires	env PHP_MIN_VERSION=%{?php_min_version} /usr/lib/rpm/php.req%{?php_req_new:.php}
