#!/usr/bin/php
<?php
/**
 * Get the Compatibility info for an entire folder (recursive)
 *
 */

require_once 'PHP/CompatInfo.php';

$info = new PHP_CompatInfo('null');

$folder  = $argv[1];
$options = array(
    'file_ext' => array('php'),
);

$res = $info->parseData($folder);
if (version_compare($res['version'], '5.0.0', 'ge')) {
	$epoch = 4;
	// produce dependencies only for php5
	$compat = false;
	// session has always been compiled in
	// date, spl are internal for php
	$staticmods = array('session', 'date', 'spl');
} else {
	$epoch = 3;
	// produce dependencies where php4/php5 both are ok
	$compat = true;
	// session has always been compiled in
	$staticmods = array('session');
}
echo "Requires:\tphp-common >= ", $epoch, ":", $res['version'], "\n";

# process extensions
foreach ($res['extensions'] as $ext) {
	if (in_array($ext, $staticmods)) {
		continue;
	}

	if ($compat) {
		echo "Requires:\tphp(", $ext, ")\n";
	} else {
		echo "Requires:\tphp-", $ext, "\n";
	}
}
