Feature: provide an easily configurable standard encryption context for different backup systems
In order to allow us to encrypt backups from different sources we
should have a common system which can manage the keys and set up for
encryption of backups.

  Background: we have prepared to run encrypted backups
        Given I have access to an account for doing backups
          and I have a private public key pair
          and the public key from that key pair is stored in an s3 bucket

  @mocked
  Scenario: prepare for backup
      Given I have a backup context configured with matching users
       When I run a backup script from that context
       Then my S3 URL should be configured
        and my encryption command should be configured

  @future
  @mocked
  Scenario: verify 
      Given I have a backup context configured with matching users
       When I request an encryption command
       Then environment variables and a script should be set up
        and the script should encrypt my data

  @future
  @mocked
  Scenario: encryption should handle multiple keys
      Given I have multiple keys for different backup users
        and I have a system for encypting backups
       When I run the backup
       Then data should be readable with any of the private keys corresponding to the public keys in the context
