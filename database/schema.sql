CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `characters` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `gsheet_link` varchar(255),
  `attr` text NOT NULL DEFAULT '{}' CHECK (json_valid(`attr`)),
  `info` text NOT NULL DEFAULT '{}' CHECK (json_valid(`info`)),
  `skills` text NOT NULL DEFAULT '{}' CHECK (json_valid(`skills`)),
  `conditions` text NOT NULL DEFAULT '{}' CHECK (json_valid(`conditions`)),
  `inventory` text NOT NULL DEFAULT '{}' CHECK (json_valid(`inventory`)),
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `server_id`)
);