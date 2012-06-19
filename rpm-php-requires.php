#!/usr/bin/php
<?php
/*
 * minify.spec does not see these: pear(HTTP/ConditionalGet.php) pear(HTTP/Encoder.php)
 * perl version does
 */
/**
 *
 * Check system dependences between php-pear modules.
 *
 * Paweł Gołaszewski <blues@pld-linux.org> (Perl version)
 * Michał Moskal <malekith@pld-linux.org> (Perl version)
 * Elan Ruusamäe <glen@pld-linux.org>
 *
 * URL: <http://cvs.pld-linux.org/cgi-bin/cvsweb.cgi/packages/rpm/rpm-php-requires.php>
 *
 * Requires: php-pear-PHP_CompatInfo
 * Requires: php-pcre
 */

/**
 * Produce pear(Path/To/File.php) deps
 * Ported to PHP from Perl version of rpm-php-requires.
 *
 * @TODO: use tokenizer to parse php files.
 */
function peardeps($files) {
	// files inside php_pear_dir have this prefix
	$prefix = RPM_BUILD_ROOT. PHP_PEAR_DIR . DIRECTORY_SEPARATOR;
	$length = strlen($prefix);

	$req = array();
	foreach ($files as $f) {
		// skip non-php files
		if (substr($f, -4) != '.php') {
			continue;
		}

		// subdir inside php_pear_dir
		if (substr($f, 0, $length) == $prefix) {
			$file_dir = dirname(substr($f, $length));
		} else {
			$file_dir = null;
		}

		foreach (file($f) as $line) {
			// skip comments -- not perfect, matches "*" at start of line (very rare altho)
			if (preg_match('/^\s*(#|\/\/|\*|\/\*)/', $line)) {
				continue;
			}

			if (preg_match("/(\W|^)(require|include)(_once)?
					\s* \(? \s*
					(\"([^\"]*)\"|'([^']*)')
					\s* \)? \s* ;/x", $line, $m)) {

				if ($m[5]) {
					$x = $m[5];
				} else if ($m[6]) {
					$x = $m[6];
				} else {
					continue 2;
				}

				if (substr($x, 0, 2) == './' || substr($x, -1) == '$') {  # XXX must be: CONTAINS DOLLAR
					continue 2;
				}

				if (substr($x, -4) != '.php') {
					continue 2;
				}
				$req[$x] = 1;
				continue 2;
			}

			if (is_null($file_dir)) {
				continue;
			}

			if (preg_match("/(\W|^)(require|include)(_once)?
					\s* \(? \s* dirname \s* \( \s* __FILE__ \s* \) \s* \. \s*
					(\"([^\"]*)\"|'([^']*)')
					\s* \)? \s* ;/x", $line, $m)) {

				if ($m[5]) {
					$x = $m[5];
				} else if ($m[6]) {
					$x = $m[6];
				} else {
					continue 2;
				}

				if (substr($x, -1) == '$') { # XXX must be: CONTAINS DOLLAR
					continue 2;
				}
				if (substr($x, -4) != '.php') {
					continue 2;
				}

				$x = "$file_dir/$x";
				// remove double slashes
				// TODO: resolve simpletest/test/../socket.php -> simpletest/socket.php
				$x = str_replace("//", "/", $x);
				$req[$x] = 1;
				continue;
			}
		}
	}

	foreach (array_keys($req) as $f) {
		// skip self deps
		if (array_key_exists($f, $files)) {
			continue;
		}
		echo "pear($f)\n";
	}
}

/**
 * Produce dependencies for extensions using PEAR PHP_CompatInfo package.
 */
function extdeps($files) {
	require_once 'PHP/CompatInfo.php';

	$info = new PHP_CompatInfo('null');
	$res = $info->parseData($files);

	// minimum php version we accept
	// "%define php_min_version 5.1.2" in spec to minimum version to be 5.1.2
	$version = max(PHP_MIN_VERSION, $res['version']);

	if (version_compare($version, '5.0.0', 'ge')) {
		# force php-<name> only deps when php5
		# XXX what about php-pecl-<name> virtual provides?
		$fmt = 'php-%s';
		$epoch = 4;
	} else {
		$fmt = 'php(%s)';
		$epoch = 3;
	}
	echo "php-common >= ", $epoch, ":", $version, "\n";

	// process extensions
	foreach ($res['extensions'] as $ext) {
		// bz2 ext is in php-bzip2 package
		if ($ext == 'bz2') {
			$ext = 'bzip2';
		}
		// libxml ext is in php-xml package
		if ($ext == 'libxml') {
			$ext = 'xml';
		}

		// these need to be lowercased
		if (in_array($ext, array('SPL', 'PDO', 'SQLite', 'Reflection', 'SimpleXML'))) {
			$ext = strtolower($ext);
		}

		printf("$fmt\n", $ext);
	}
}

define('RPM_BUILD_ROOT', getenv('RPM_BUILD_ROOT'));
define('PHP_PEAR_DIR', '/usr/share/pear');
define('PHP_MIN_VERSION', getenv('PHP_MIN_VERSION'));

if ($argc > 1) {
	$files = array_splice($argv, 1);
} else {
	$files = explode(PHP_EOL, trim(file_get_contents('php://stdin')));
}

peardeps($files);
extdeps($files);
