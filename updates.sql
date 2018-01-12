CREATE TABLE `updates` (
  `file_version` int(11) NOT NULL,
  `filename` varchar(32) NOT NULL,
  `file_hash` varchar(32) NOT NULL,
  `filesize` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `patch_id` int(11) DEFAULT NULL,
  `url_full` varchar(128) NOT NULL,
  `url_patch` varchar(128) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

ALTER TABLE `updates`
  ADD PRIMARY KEY (`file_version`);