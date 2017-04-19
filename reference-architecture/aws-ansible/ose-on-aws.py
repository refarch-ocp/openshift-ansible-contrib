#!/usr/bin/env python
# vim: sw=2 ts=2

import click
import os
import sys

@click.command()

### Cluster options
@click.option('--stack-name', default='openshift-infra', help='Cloudformation stack name. Must be unique',
              show_default=True)
@click.option('--console-port', default='443', type=click.IntRange(1,65535), help='OpenShift web console port',
              show_default=True)
@click.option('--deployment-type', default='openshift-enterprise', type=click.Choice(['origin', 'openshift-enterprise']),  help='OpenShift deployment type',
              show_default=True)
@click.option('--openshift-sdn', default='openshift-ovs-subnet', type=click.Choice(['openshift-ovs-subnet', 'openshift-ovs-multitenant']),  help='OpenShift SDN',
              show_default=True)

### AWS/EC2 options
@click.option('--region', default='us-east-1', help='ec2 region',
              show_default=True)
@click.option('--ami', default='ami-a33668b4', help='ec2 ami',
              show_default=True)
@click.option('--master-instance-type', default='m4.large', help='ec2 instance type',
              show_default=True)
@click.option('--node-instance-type', default='t2.medium', help='ec2 instance type',
              show_default=True)
@click.option('--app-instance-type', default='t2.medium', help='ec2 instance type',
              show_default=True)
@click.option('--bastion-instance-type', default='t2.micro', help='ec2 instance type',
              show_default=True)
@click.option('--keypair', help='ec2 keypair name',
              show_default=True)
@click.option('--create-key', default='no', help='Create SSH keypair',
              show_default=True)
@click.option('--key-path', default='/dev/null', help='Path to SSH public key. Default is /dev/null which will skip the step',
              show_default=True)
@click.option('--create-vpc', default='yes', help='Create VPC',
              show_default=True)
@click.option('--vpc-id', help='Specify an already existing VPC',
              show_default=True)
@click.option('--vpc-default-nameserver', help='VPC Default Nameserver',
              show_default=True)
@click.option('--private-subnet-id1', help='Specify a Private subnet within the existing VPC',
              show_default=True)
@click.option('--private-subnet-id2', help='Specify a Private subnet within the existing VPC',
              show_default=True)
@click.option('--private-subnet-id3', help='Specify a Private subnet within the existing VPC',
              show_default=True)

### DNS options
@click.option('--public-hosted-zone', help='hosted zone for accessing the environment')
@click.option('--cluster-shortname', help='ocp cluster shortname')
@click.option('--master-hostname-01', help='master hostname 01')
@click.option('--master-hostname-02', help='master hostname 02')
@click.option('--master-hostname-03', help='master hostname 03')
@click.option('--app-hostname-01', help='app hostname 01')
@click.option('--app-hostname-02', help='app hostname 02')
@click.option('--app-hostname-03', help='app hostname 03')
@click.option('--infrarouter-hostname-01', help='infrarouter hostname 01')
@click.option('--infrarouter-hostname-02', help='infrarouter hostname 02')
@click.option('--infrarouter-hostname-03', help='infrarouter hostname 03')
@click.option('--infraregistry-hostname-01', help='infraregistry hostname 01')
@click.option('--infraregistry-hostname-02', help='infraregistry hostname 02')
@click.option('--infraregistry-hostname-03', help='infraregistry hostname 03')
@click.option('--infragluster-hostname-01', help='infragluster hostname 01')
@click.option('--infragluster-hostname-02', help='infragluster hostname 02')
@click.option('--infragluster-hostname-03', help='infragluster hostname 03')
@click.option('--app-dns-prefix', default='apps', help='application dns prefix',
              show_default=True)

### Subscription and Software options

### Miscellaneous options
@click.option('--byo-bastion', default='no', help='skip bastion install when one exists within the cloud provider',
              show_default=True)
@click.option('--bastion-sg', default='/dev/null', help='Specify Bastion Security group used with byo-bastion',
              show_default=True)
@click.option('--containerized', default='False', help='Containerized installation of OpenShift',
              show_default=True)
@click.option('--s3-bucket-name', help='Bucket name for S3 for registry')
@click.option('--s3-username',  help='S3 user for registry access')
@click.option('--sat-bootstrap-rpm',  help='Satellite Bootstrap RPM URL')
@click.option('--rhsm-activation-key',  help='OCP satellite default activation key')
@click.option('--rhsm-org-id',  help='OCP satellite org id')
@click.option('--rhsm-server-hostname',  help='RHSM Server Hostname')
@click.option('--rhsm-gluster-activation-key',  help='OCP satellite gluster activation key')
@click.option('--no-confirm', is_flag=True,
              help='Skip confirmation prompt')
@click.help_option('--help', '-h')
@click.option('-v', '--verbose', count=True)

def launch_refarch_env(region=None,
                    stack_name=None,
                    ami=None,
                    no_confirm=False,
                    master_instance_type=None,
                    node_instance_type=None,
                    app_instance_type=None,
                    bastion_instance_type=None,
                    keypair=None,
                    create_key=None,
                    key_path=None,
                    create_vpc=None,
                    vpc_id=None,
                    vpc_default_nameserver=None,
                    private_subnet_id1=None,
                    private_subnet_id2=None,
                    private_subnet_id3=None,
                    byo_bastion=None,
                    bastion_sg=None,
                    public_hosted_zone=None,
                    cluster_shortname=None,
                    master_hostname_01=None,
                    master_hostname_02=None,
                    master_hostname_03=None,
                    app_hostname_01=None,
                    app_hostname_02=None,
                    app_hostname_03=None,
                    infrarouter_hostname_01=None,
                    infrarouter_hostname_02=None,
                    infrarouter_hostname_03=None,
                    infraregistry_hostname_01=None,
                    infraregistry_hostname_02=None,
                    infraregistry_hostname_03=None,
                    infragluster_hostname_01=None,
                    infragluster_hostname_02=None,
                    infragluster_hostname_03=None,
                    app_dns_prefix=None,
                    deployment_type=None,
                    openshift_sdn=None,
                    console_port=443,
                    containerized=None,
                    s3_bucket_name=None,
                    s3_username=None,
                    sat_bootstrap_rpm=None,
                    rhsm_activation_key=None,
										rhsm_org_id=None,
										rhsm_server_hostname=None,
                    rhsm_gluster_activation_key=None,
                    verbose=1):

  # Need to prompt for the R53 zone:
  if public_hosted_zone is None:
    public_hosted_zone = click.prompt('Hosted DNS zone for accessing the environment')

  if cluster_shortname is None:
    cluster_shortname = click.prompt('Please enter cluster name')

  if master_hostname_01 is None:
    master_hostname_01 = click.prompt('Please set master hostname 01 FQDN')

  if master_hostname_02 is None:
    master_hostname_02 = click.prompt('Please set master hostname 02 FQDN')

  if master_hostname_03 is None:
    master_hostname_03 = click.prompt('Please set master hostname 03 FQDN')

  if app_hostname_01 is None:
    app_hostname_01 = click.prompt('Please set app hostname 01 FQDN')

  if app_hostname_02 is None:
    app_hostname_02 = click.prompt('Please set app hostname 02 FQDN')

  if app_hostname_03 is None:
    app_hostname_03 = click.prompt('Please set app hostname 03 FQDN')

  if infrarouter_hostname_01 is None:
    infrarouter_hostname_01 = click.prompt('Please set infrarouter hostname 01 FQDN')

  if infrarouter_hostname_02 is None:
    infrarouter_hostname_02 = click.prompt('Please set infrarouter hostname 02 FQDN')

  if infrarouter_hostname_03 is None:
    infrarouter_hostname_03 = click.prompt('Please set infrarouter hostname 03 FQDN')

  if infraregistry_hostname_01 is None:
    infraregistry_hostname_01 = click.prompt('Please set infraregistry hostname 01 FQDN')

  if infraregistry_hostname_02 is None:
    infraregistry_hostname_02 = click.prompt('Please set infraregistry hostname 02 FQDN')

  if infraregistry_hostname_03 is None:
    infraregistry_hostname_03 = click.prompt('Please set infraregistry hostname 03 FQDN')

  if infragluster_hostname_01 is None:
    infragluster_hostname_01 = click.prompt('Please set infragluster hostname 01 FQDN')

  if infragluster_hostname_02 is None:
    infragluster_hostname_02 = click.prompt('Please set infragluster hostname 02 FQDN')

  if infragluster_hostname_03 is None:
    infragluster_hostname_03 = click.prompt('Please set infragluster hostname 03 FQDN')

  if s3_bucket_name is None:
    s3_bucket_name = stack_name + '-ocp-registry-' + public_hosted_zone.split('.')[0]

  if s3_username is None:
    s3_username = stack_name + '-s3-openshift-user'

  # Create ssh key pair in AWS if none is specified
  if create_key in 'yes' and key_path in 'no':
    key_path = click.prompt('Specify path for ssh public key')
    keypair = click.prompt('Specify a name for the keypair')

 # If no keypair is not specified fail:
  if keypair is None and create_key in 'no':
    click.echo('A SSH keypair must be specified or created')
    sys.exit(1)

 # Name the keypair if a path is defined
  if keypair is None and create_key in 'yes':
    keypair = click.prompt('Specify a name for the keypair')

 # If no subnets are defined prompt:
  if create_vpc in 'no' and vpc_id is None:
    vpc_id = click.prompt('Specify the VPC ID')

  if create_vpc in 'no' and vpc_default_nameserver is None:
    vpc_default_nameserver = click.prompt('Specify the VPC Default Nameserver')

 # If no subnets are defined prompt:
  if create_vpc in 'no' and private_subnet_id1 is None:
    private_subnet_id1 = click.prompt('Specify the first Private subnet within the existing VPC')
    private_subnet_id2 = click.prompt('Specify the second Private subnet within the existing VPC')
    private_subnet_id3 = click.prompt('Specify the third Private subnet within the existing VPC')

 # Prompt for Bastion SG if byo-bastion specified
  #if byo_bastion in 'yes' and bastion_sg in '/dev/null':
    #bastion_sg = click.prompt('Specify the the Bastion Security group(example: sg-4afdd24)')

  # If the user already provided values, don't bother asking again
  #if deployment_type in ['openshift-enterprise'] and rhsm_user is None:
  #  rhsm_user = click.prompt("RHSM username?")
  #if deployment_type in ['openshift-enterprise'] and rhsm_password is None:
  #  rhsm_password = click.prompt("RHSM password?", hide_input=True)
  #if deployment_type in ['openshift-enterprise'] and rhsm_pool is None:
  #  rhsm_pool = click.prompt("RHSM Pool ID or Subscription Name?")
  if deployment_type in ['openshift-enterprise'] and rhsm_activation_key is None:
     rhsm_activation_key = click.prompt("RHSM activation_key?")
  if deployment_type in ['openshift-enterprise'] and rhsm_org_id is None:
     rhsm_org_id = click.prompt("RHSM org id?")
     rhsm_server_hostname = click.prompt("RHSM server hostname?")
  if deployment_type in ['openshift-enterprise'] and sat_bootstrap_rpm is None:
     sat_bootstrap_rpm = click.prompt("Satellite bootstrap rpm url")

  # Calculate various DNS values
  wildcard_zone="%s.%s" % (app_dns_prefix, public_hosted_zone)

  # GitHub Authentication
  #if github_organization is None or not github_organization:
  #  click.echo('A GitHub organization must be provided')
  #  sys.exit(1)
  #if github_client_id is None:
  #  github_client_id = click.prompt('Specify the ClientID for GitHub OAuth')
  #if github_client_secret is None:
  #  github_client_secret = click.prompt('Specify the Client Secret for GitHub OAuth')

  #if isinstance(github_organization, str) or isinstance(github_organization, unicode):
  #  github_organization = [github_organization]

  # Display information to the user about their choices
  click.echo('Configured values:')
  click.echo('\tstack_name: %s' % stack_name)
  click.echo('\tami: %s' % ami)
  click.echo('\tregion: %s' % region)
  click.echo('\tmaster_instance_type: %s' % master_instance_type)
  click.echo('\tnode_instance_type: %s' % node_instance_type)
  click.echo('\tapp_instance_type: %s' % app_instance_type)
  click.echo('\tbastion_instance_type: %s' % bastion_instance_type)
  click.echo('\tkeypair: %s' % keypair)
  click.echo('\tcreate_key: %s' % create_key)
  click.echo('\tkey_path: %s' % key_path)
  click.echo('\tcreate_vpc: %s' % create_vpc)
  click.echo('\tvpc_id: %s' % vpc_id)
  click.echo('\tvpc_default_nameserver: %s' % vpc_default_nameserver)
  click.echo('\tprivate_subnet_id1: %s' % private_subnet_id1)
  click.echo('\tprivate_subnet_id2: %s' % private_subnet_id2)
  click.echo('\tprivate_subnet_id3: %s' % private_subnet_id3)
  click.echo('\tbyo_bastion: %s' % byo_bastion)
  click.echo('\tbastion_sg: %s' % bastion_sg)
  click.echo('\tconsole port: %s' % console_port)
  click.echo('\tdeployment_type: %s' % deployment_type)
  click.echo('\topenshift_sdn: %s' % openshift_sdn)
  click.echo('\tpublic_hosted_zone: %s' % public_hosted_zone)
  click.echo('\tcluster_shortname: %s' % cluster_shortname)
  click.echo('\tmaster_hostname_01: %s' % master_hostname_01)
  click.echo('\tmaster_hostname_02: %s' % master_hostname_02)
  click.echo('\tmaster_hostname_03: %s' % master_hostname_03)
  click.echo('\tapp_hostname_01: %s' % app_hostname_01)
  click.echo('\tapp_hostname_02: %s' % app_hostname_02)
  click.echo('\tapp_hostname_03: %s' % app_hostname_03)
  click.echo('\tinfrarouter_hostname_01: %s' % infrarouter_hostname_01)
  click.echo('\tinfrarouter_hostname_02: %s' % infrarouter_hostname_02)
  click.echo('\tinfrarouter_hostname_03: %s' % infrarouter_hostname_03)
  click.echo('\tinfraregistry_hostname_01: %s' % infraregistry_hostname_01)
  click.echo('\tinfraregistry_hostname_02: %s' % infraregistry_hostname_02)
  click.echo('\tinfraregistry_hostname_03: %s' % infraregistry_hostname_03)
  click.echo('\tinfragluster_hostname_01: %s' % infragluster_hostname_01)
  click.echo('\tinfragluster_hostname_02: %s' % infragluster_hostname_02)
  click.echo('\tinfragluster_hostname_03: %s' % infragluster_hostname_03)
  click.echo('\tapp_dns_prefix: %s' % app_dns_prefix)
  click.echo('\tapps_dns: %s' % wildcard_zone)
  click.echo('\tcontainerized: %s' % containerized)
  click.echo('\ts3_bucket_name: %s' % s3_bucket_name)
  click.echo('\ts3_username: %s' % s3_username)
  click.echo('\tsat_bootstrap_rpm: %s' % sat_bootstrap_rpm)
  click.echo('\trhsm_activation_key: %s' % rhsm_activation_key)
  click.echo('\trhsm_org_id: %s' % rhsm_org_id)
  click.echo('\trhsm_server_hostname: %s' % rhsm_server_hostname)
  click.echo('\trhsm_gluster_activation_key: %s' % rhsm_gluster_activation_key)
  click.echo("")

  if not no_confirm:
    click.confirm('Continue using these values?', abort=True)

  playbooks = ['playbooks/infrastructure.yaml', 'playbooks/openshift-install.yaml']
  #playbooks = ['playbooks/infrastructure.yaml']
  #playbooks = ['playbooks/openshift-install.yaml']

  for playbook in playbooks:

    # hide cache output unless in verbose mode
    devnull='> /dev/null'

    if verbose > 0:
      devnull=''

    # refresh the inventory cache to prevent stale hosts from
    # interferring with re-running
    command='inventory/aws/hosts/ec2.py --refresh-cache %s' % (devnull)
    os.system(command)

    # remove any cached facts to prevent stale data during a re-run
    command='rm -rf .ansible/cached_facts'
    os.system(command)

    command='ansible-playbook -vvv -i inventory/aws/hosts -e \'region=%s \
    add_node=no \
    stack_name=%s \
    ami=%s \
    keypair=%s \
    create_key=%s \
    key_path=%s \
    create_vpc=%s \
    vpc_id=%s \
    vpc_default_nameserver=%s \
    private_subnet_id1=%s \
    private_subnet_id2=%s \
    private_subnet_id3=%s \
    byo_bastion=%s \
    bastion_sg=%s \
    master_instance_type=%s \
    node_instance_type=%s \
    app_instance_type=%s \
    bastion_instance_type=%s \
    public_hosted_zone=%s \
    cluster_shortname=%s \
    master_hostname_01=%s \
    master_hostname_02=%s \
    master_hostname_03=%s \
    app_hostname_01=%s \
    app_hostname_02=%s \
    app_hostname_03=%s \
    infrarouter_hostname_01=%s \
    infrarouter_hostname_02=%s \
    infrarouter_hostname_03=%s \
    infraregistry_hostname_01=%s \
    infraregistry_hostname_02=%s \
    infraregistry_hostname_03=%s \
    infragluster_hostname_01=%s \
    infragluster_hostname_02=%s \
    infragluster_hostname_03=%s \
    wildcard_zone=%s \
    console_port=%s \
    deployment_type=%s \
    openshift_sdn=%s \
    containerized=%s \
    s3_bucket_name=%s \
    s3_username=%s \
    sat_bootstrap_rpm=%s \
    rhsm_activation_key=%s \
    rhsm_org_id=%s \
    rhsm_server_hostname=%s \
    rhsm_gluster_activation_key=%s\' %s' % (region,
										stack_name,
                    ami,
                    keypair,
                    create_key,
                    key_path,
                    create_vpc,
                    vpc_id,
                    vpc_default_nameserver,
                    private_subnet_id1,
                    private_subnet_id2,
                    private_subnet_id3,
                    byo_bastion,
                    bastion_sg,
                    master_instance_type,
                    node_instance_type,
                    app_instance_type,
                    bastion_instance_type,
                    public_hosted_zone,
                    cluster_shortname,
                    master_hostname_01,
                    master_hostname_02,
                    master_hostname_03,
                    app_hostname_01,
                    app_hostname_02,
                    app_hostname_03,
                    infrarouter_hostname_01,
                    infrarouter_hostname_02,
                    infrarouter_hostname_03,
                    infraregistry_hostname_01,
                    infraregistry_hostname_02,
                    infraregistry_hostname_03,
                    infragluster_hostname_01,
                    infragluster_hostname_02,
                    infragluster_hostname_03,
                    wildcard_zone,
									  console_port,
                    deployment_type,
                    openshift_sdn,
                    containerized,
                    s3_bucket_name,
                    s3_username,
                    sat_bootstrap_rpm,
                    rhsm_activation_key,
                    rhsm_org_id,
                    rhsm_server_hostname,
                    rhsm_gluster_activation_key,
                    playbook)
         

    if verbose > 0:
      command += " -" + "".join(['v']*verbose)
      click.echo('We are running: %s' % command)

    status = os.system(command)
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
      sys.exit(os.WEXITSTATUS(status))


if __name__ == '__main__':
  # check for AWS access info
  if os.getenv('AWS_ACCESS_KEY_ID') is None or os.getenv('AWS_SECRET_ACCESS_KEY') is None:
    print 'AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY **MUST** be exported as environment variables.'
    sys.exit(1)

  launch_refarch_env(auto_envvar_prefix='OSE_REFArch')
