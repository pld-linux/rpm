#!/usr/bin/php
<?php
/**
 *
 * Check system dependences between php-pear modules.
 * Based on Perl version rpm-php-requires.
 *
 * Paweł Gołaszewski <blues@pld-linux.org>
 * Michał Moskal <malekith@pld-linux.org>
 * Elan Ruusamäe <glen@pld-linux.org>
 */

/**
 * Produce old style pear(Path/To/File.php) deps
 */
function peardeps($files) {
	// all files must begin with $RPM_BUILD_ROOT%{php_pear_dir}
	$prefix = RPM_BUILD_ROOT. PHP_PEAR_DIR . DIRECTORY_SEPARATOR;
	$length = strlen($prefix);
	foreach ($files as $f) {
		if (substr($f, 0, $length) != $prefix) {
			continue;
		}
		$f = substr($f, $length);
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

	if (version_compare($res['version'], '5.0.0', 'ge')) {
		$epoch = 4;
		// session, pcre are statically compiled in
		// date, SPL, SimpleXML are internal for php
		// sapi_apache?
		$staticmods = array('standard', 'ereg', 'session', 'pcre', 'date', 'spl', 'simplexml');
	} else {
		$epoch = 3;
		// session has always been compiled in
		$staticmods = array('standard', 'ereg', 'session');
	}
	echo "php-common >= ", $epoch, ":", $res['version'], "\n";

	// process extensions
	foreach ($res['extensions'] as $ext) {
		if (in_array($ext, $staticmods)) {
			continue;
		}

		echo "php(", $ext, ")\n";
	}
}

define('RPM_BUILD_ROOT', getenv('RPM_BUILD_ROOT'));
define('PHP_PEAR_DIR', '/usr/share/pear');

if ($argc > 1) {
	$files = array_splice($argv, 1);
} else {
	$files = split(PHP_EOL, trim(file_get_contents('php://stdin')));
}

peardeps($files);
extdeps($files);
