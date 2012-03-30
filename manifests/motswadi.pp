# Globally set exec paths and user.
Exec {
    path => ["/bin", "/usr/bin", "/usr/local/bin"],
    user => 'ubuntu',
}

# Update package index.
exec { "update_apt":
    command => "apt-get update",
    user => "root",
}

# Install required packages.
package { [
    "git-core",
    "libpq-dev",
    "nginx",
    "postgresql",
    "python-dev",
#    "python-pip",
    "python-virtualenv",
    "supervisor",
    ]:
    ensure => latest,
    subscribe => Exec['update_apt'];
}

# Ensure Ubuntu user exists
user { "ubuntu":
    ensure => "present",
    home => "/home/ubuntu",
    shell => "/bin/bash"
}

# Create the deployment directory
file { "/var/praekelt/":
    ensure => "directory",
    owner => "ubuntu",
    subscribe => User["ubuntu"]
}

# Clone and update repo.
exec { "clone_repo":
    command => "git clone https://github.com/praekelt/motswadi.git motswadi",
    cwd => "/var/praekelt",
    unless => "test -d /var/praekelt/motswadi",
    subscribe => [
        Package['git-core'],
        File['/var/praekelt/'],
    ]
}

exec { "update_repo":
    command => "git pull origin",
    cwd => "/var/praekelt/motswadi",
    subscribe => [
        Exec['clone_repo'],
    ]
}

# Create virtualenv.
exec { 'create_virtualenv':
    command => 'virtualenv --no-site-packages ve',
    cwd => '/var/praekelt/motswadi',
    unless => 'test -d /var/praekelt/motswadi/ve',
    subscribe => [
        Package['libpq-dev'],
        Package['python-dev'],
        Package['python-virtualenv'],
        Exec['clone_repo'],
    ]
}

# Install python packages.
exec { 'install_packages':
    command => '. ve/bin/activate && pip install -r requirements.pip && deactivate',
    cwd => '/var/praekelt/motswadi',
    subscribe => [
        Exec['create_virtualenv'],
        Exec['update_repo'],
    ]
}

# Manage Nginx symlinks.
file { "/etc/nginx/sites-enabled/motswadi.conf":
    ensure => symlink,
    target => "/var/praekelt/motswadi/nginx/motswadi.conf",
    require => [
        Exec['update_repo'],
        Package['nginx'],
    ]
}

#file { "/etc/nginx/sites-enabled/default":
#    ensure => absent,
#    subscribe => [
#        Package['nginx'],
#    ]
#}

# Manage supervisord symlinks.
file { "/etc/supervisor/conf.d/motswadi.fcgi":
    ensure => symlink,
    target => "/var/praekelt/motswadi/supervisord/motswadi.fcgi",
    subscribe => [
        Exec['update_repo'],
        Package['supervisor']
    ]
}

# Create Postgres role and database.
postgres::role { "motswadi":
    password => motswadi,
    ensure => present,
    subscribe => Package["postgresql"],
}

postgres::database { "motswadi":
    owner => motswadi,
    ensure => present,
    template => "template0",
}
