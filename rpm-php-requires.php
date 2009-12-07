#!/usr/bin/php
<?php
/**
 *
 * Check system dependences between php-pear modules.
 *
 * Paweł Gołaszewski <blues@pld-linux.org> (Perl version)
 * Michał Moskal <malekith@pld-linux.org> (Perl version)
 * Elan Ruusamäe <glen@pld-linux.org>
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
			// skip comments
			if (preg_match('/^\s*(#|\/\/|\*|\/\*)/', $line)) {
				continue;
			}

			while (preg_match("/(\W|^)(require|include)(_once)?
					\s* \(? \s*
					(\"([^\"]*)\"|'([^']*)')
					\s* \)? \s* ;/x", $line, $m)) {

				if ($m[5] != "") {
					$x = $m[5];
				} else if ($m[6] != "") {
					$x = $m[6];
				} else {
					continue 2;
				}

				if (substr($x, 0, 2) == './' || substr($x, -1) == '$') {
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

			while (preg_match("/(\W|^)(require|include)(_once)?
					\s* \(? \s* dirname \s* \( \s* __FILE__ \s* \) \s* \. \s*
					(\"([^\"]*)\"|'([^']*)')
					\s* \)? \s* ;/x", $line, $m)) {

				if ($m[5] != "") {
					$x = $m[5];
				} else if ($m[6] != "") {
					$x = $m[6];
				} else {
					continue 2;
				}

				if (substr($x, -1) == '$') {
					continue 2;
				}
				if (substr($x, -4) != '.php') {
					continue 2;
				}

				$x = "$file_dir/$x";
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

	if (version_compare($res['version'], '5.0.0', 'ge')) {
		$epoch = 4;
	} else {
		$epoch = 3;
	}
	echo "php-common >= ", $epoch, ":", $res['version'], "\n";

	// process extensions
	foreach ($res['extensions'] as $ext) {
		// bz2 ext is in php-bzip2 package
		if ($ext == 'bz2') {
			$ext = 'bzip2';
		}
		echo "php(", $ext, ")\n";
	}
}

define('RPM_BUILD_ROOT', getenv('RPM_BUILD_ROOT'));
define('PHP_PEAR_DIR', '/usr/share/pear');

if ($argc > 1) {
	$files = array_splice($argv, 1);
} else {
	$files = explode(PHP_EOL, trim(file_get_contents('php://stdin')));
}

peardeps($files);
extdeps($files);
