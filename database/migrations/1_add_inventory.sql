ALTER TABLE `characters` ADD COLUMN `inventory` text NOT NULL DEFAULT '{}' CHECK (json_valid(`inventory`));
