<?xml version='1.0' encoding='UTF-8'?>

<server xmlns="urn:jboss:domain:9.0">
    <extensions>
        <extension module="org.jboss.as.clustering.infinispan"/>
        <extension module="org.jboss.as.clustering.jgroups"/>
        <extension module="org.jboss.as.connector"/>
        <extension module="org.jboss.as.deployment-scanner"/>
        <extension module="org.jboss.as.ee"/>
        <extension module="org.jboss.as.ejb3"/>
        <extension module="org.jboss.as.jaxrs"/>
        <extension module="org.jboss.as.jmx"/>
        <extension module="org.jboss.as.jpa"/>
        <extension module="org.jboss.as.logging"/>
        <extension module="org.jboss.as.mail"/>
        <extension module="org.jboss.as.modcluster"/>
        <extension module="org.jboss.as.naming"/>
        <extension module="org.jboss.as.remoting"/>
        <extension module="org.jboss.as.security"/>
        <extension module="org.jboss.as.transactions"/>
        <extension module="org.jboss.as.weld"/>
        <extension module="org.keycloak.keycloak-server-subsystem"/>
        <extension module="org.wildfly.extension.bean-validation"/>
        <extension module="org.wildfly.extension.core-management"/>
        <extension module="org.wildfly.extension.elytron"/>
        <extension module="org.wildfly.extension.io"/>
        <extension module="org.wildfly.extension.microprofile.config-smallrye"/>
        <extension module="org.wildfly.extension.microprofile.health-smallrye"/>
        <extension module="org.wildfly.extension.microprofile.metrics-smallrye"/>
        <extension module="org.wildfly.extension.request-controller"/>
        <extension module="org.wildfly.extension.security.manager"/>
        <extension module="org.wildfly.extension.undertow"/>
    </extensions>
    <management>
        <security-realms>
            <security-realm name="ManagementRealm">
                <authentication>
                    <local default-user="$local" skip-group-loading="true"/>
                    <properties path="mgmt-users.properties" relative-to="jboss.server.config.dir"/>
                </authentication>
                <authorization map-groups-to-roles="false">
                    <properties path="mgmt-groups.properties" relative-to="jboss.server.config.dir"/>
                </authorization>
            </security-realm>
            <security-realm name="ApplicationRealm">
                <authentication>
                    <local default-user="$local" allowed-users="*" skip-group-loading="true"/>
                    <properties path="application-users.properties" relative-to="jboss.server.config.dir"/>
                </authentication>
                <authorization>
                    <properties path="application-roles.properties" relative-to="jboss.server.config.dir"/>
                </authorization>
                <server-identities>
                    <ssl>
                        <keystore  path="/etc/eap-secret-volume/keystore.jks" keystore-password="redhat"/>
                    </ssl>
                </server-identities>
            </security-realm>
        </security-realms>
        <audit-log>
            <formatters>
                <json-formatter name="json-formatter"/>
            </formatters>
            <handlers>
                <file-handler name="file" formatter="json-formatter" path="audit-log.log" relative-to="jboss.server.data.dir"/>
            </handlers>
            <logger log-boot="true" log-read-only="false" enabled="false">
                <handlers>
                    <handler name="file"/>
                </handlers>
            </logger>
        </audit-log>
        <management-interfaces>
            <http-interface console-enabled="false"><!-- ##MGMT_IFACE_REALM## -->
                <http-upgrade enabled="true"/>
                <socket-binding http="management-http"/>
            </http-interface>
        </management-interfaces>
        <access-control provider="simple">
            <role-mapping>
                <role name="SuperUser">
                    <include>
                        <user name="$local"/>
                    </include>
                </role>
            </role-mapping>
        </access-control>
    </management>
    <profile>
        <subsystem xmlns="urn:jboss:domain:logging:6.0">
            <console-handler name="CONSOLE">
                <formatter>
                    <named-formatter name="COLOR-PATTERN"/>
                </formatter>
            </console-handler>
            <logger category="com.arjuna">
                <level name="WARN"/>
            </logger>
            <logger category="org.jboss.as.config">
                <level name="DEBUG"/>
            </logger>
            <logger category="sun.rmi">
                <level name="WARN"/>
            </logger>
            <root-logger>
                <level name="INFO"/>
                <handlers>
                    <handler name="CONSOLE"/>
                </handlers>
            </root-logger>
            <formatter name="OPENSHIFT">
                <json-formatter>
                    <exception-output-type value="formatted"/>
                    <key-overrides timestamp="@timestamp"/>
                    <meta-data>
                        <property name="@version" value="1"/>
                    </meta-data>
                </json-formatter>
            </formatter>
            <formatter name="COLOR-PATTERN">
                <pattern-formatter pattern="%K{level}%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%e%n"/>
            </formatter>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:bean-validation:1.0"/>
        <subsystem xmlns="urn:jboss:domain:core-management:1.0"/>
        <subsystem xmlns="urn:jboss:domain:datasources:5.0">
            <datasources>
                <xa-datasource jndi-name="java:jboss/datasources/KeycloakDS" pool-name="sso_postgresql-DB" enabled="true" use-java-context="true" statistics-enabled="${wildfly.datasources.statistics-enabled:${wildfly.statistics-enabled:false}}"> <xa-datasource-property name="DatabaseName">ssodb</xa-datasource-property> <xa-datasource-property name="ServerName">ssodb.pgo.svc.cluster.local</xa-datasource-property> <driver>postgresql</driver> <security> <user-name>admin</user-name> <password>Aa123456</password> </security> </xa-datasource>
<!-- ##DATASOURCES## -->
                <datasource jndi-name="java:jboss/datasources/ExampleDS" pool-name="ExampleDS" enabled="true" use-java-context="true">
                    <connection-url>jdbc:h2:mem:test;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE</connection-url>
                    <driver>h2</driver>
                    <security>
                        <user-name>sa</user-name>
                        <password>sa</password>
                    </security>
                </datasource>
                <drivers>
                    <driver name="h2" module="com.h2database.h2">
                        <xa-datasource-class>org.h2.jdbcx.JdbcDataSource</xa-datasource-class>
                    </driver>
                    <driver name="postgresql" module="org.postgresql">
                        <xa-datasource-class>org.postgresql.xa.PGXADataSource</xa-datasource-class>
                    </driver>
                    <!-- ##DRIVERS## -->
                </drivers>
            </datasources>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:deployment-scanner:2.0">
            <deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000" runtime-failure-causes-rollback="${jboss.deployment.scanner.rollback.on.failure:false}" auto-deploy-exploded="false"/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:ee:4.0">
            <spec-descriptor-property-replacement>false</spec-descriptor-property-replacement>
            <concurrent>
                <context-services>
                    <context-service name="default" jndi-name="java:jboss/ee/concurrency/context/default" use-transaction-setup-provider="true"/>
                </context-services>
                <managed-thread-factories>
                    <managed-thread-factory name="default" jndi-name="java:jboss/ee/concurrency/factory/default" context-service="default"/>
                </managed-thread-factories>
                <managed-executor-services>
                    <managed-executor-service name="default" jndi-name="java:jboss/ee/concurrency/executor/default" context-service="default" hung-task-threshold="60000" keepalive-time="5000"/>
                </managed-executor-services>
                <managed-scheduled-executor-services>
                    <managed-scheduled-executor-service name="default" jndi-name="java:jboss/ee/concurrency/scheduler/default" context-service="default" hung-task-threshold="60000" keepalive-time="3000"/>
                </managed-scheduled-executor-services>
            </concurrent>
            <default-bindings context-service="java:jboss/ee/concurrency/context/default"
                              datasource="java:jboss/datasources/KeycloakDS"
                              jms-connection-factory="java:jboss/DefaultJMSConnectionFactory"
                              managed-executor-service="java:jboss/ee/concurrency/executor/default"
                              managed-scheduled-executor-service="java:jboss/ee/concurrency/scheduler/default"
                              managed-thread-factory="java:jboss/ee/concurrency/factory/default"/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:ejb3:6.0">
            <session-bean>
                <stateless>
                    <bean-instance-pool-ref pool-name="slsb-strict-max-pool"/>
                </stateless>
                <stateful default-access-timeout="5000" cache-ref="distributable" passivation-disabled-cache-ref="simple"/>
                <singleton default-access-timeout="5000"/>
            </session-bean>
            <pools>
                <bean-instance-pools>
                    <strict-max-pool name="mdb-strict-max-pool" derive-size="from-cpu-count" instance-acquisition-timeout="5" instance-acquisition-timeout-unit="MINUTES"/>
                    <strict-max-pool name="slsb-strict-max-pool" derive-size="from-worker-pools" instance-acquisition-timeout="5" instance-acquisition-timeout-unit="MINUTES"/>
                </bean-instance-pools>
            </pools>
            <caches>
                <cache name="simple"/>
                <cache name="distributable" passivation-store-ref="infinispan" aliases="passivating clustered"/>
            </caches>
            <passivation-stores>
                <passivation-store name="infinispan" cache-container="ejb" max-size="10000"/>
            </passivation-stores>
            <async thread-pool-name="default"/>
            <timer-service thread-pool-name="default" default-data-store="default-file-store">
                <data-stores>
                    <file-data-store name="default-file-store" path="timer-service-data" relative-to="jboss.server.data.dir"/>
                </data-stores>
            </timer-service>
            <remote connector-ref="http-remoting-connector" thread-pool-name="default">
                <channel-creation-options>
                    <option name="READ_TIMEOUT" value="${prop.remoting-connector.read.timeout:20}" type="xnio"/>
                    <option name="MAX_OUTBOUND_MESSAGES" value="1234" type="remoting"/>
                </channel-creation-options>
            </remote>
            <thread-pools>
                <thread-pool name="default">
                    <max-threads count="10"/>
                    <keepalive-time time="100" unit="milliseconds"/>
                </thread-pool>
            </thread-pools>
            <default-security-domain value="other"/>
            <default-missing-method-permissions-deny-access value="true"/>
            <log-system-exceptions value="true"/>
            <!-- ##EJB_APPLICATION_SECURITY_DOMAINS## -->
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:io:3.0">
            <worker name="default"/>
            <buffer-pool name="default"/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:infinispan:9.0">
            <cache-container name="keycloak">
                <transport lock-timeout="60000"/>
                <local-cache name="realms">
                    <object-memory size="10000"/>
                </local-cache>
                <local-cache name="users">
                    <object-memory size="10000"/>
                </local-cache>
                <distributed-cache name="sessions" owners="1"/>
                <distributed-cache name="authenticationSessions" owners="1"/>
                <distributed-cache name="offlineSessions" owners="1"/>
                <distributed-cache name="clientSessions" owners="1"/>
                <distributed-cache name="offlineClientSessions" owners="1"/>
                <distributed-cache name="loginFailures" owners="1"/>
                <local-cache name="authorization">
                    <object-memory size="10000"/>
                </local-cache>
                <replicated-cache name="work"/>
                <local-cache name="keys">
                    <object-memory size="1000"/>
                    <expiration max-idle="3600000"/>
                </local-cache>
                <distributed-cache name="actionTokens" owners="2">
                    <object-memory size="-1"/>
                    <expiration max-idle="-1" interval="300000"/>
                </distributed-cache>
            </cache-container>
            <cache-container name="server" aliases="singleton cluster" default-cache="default" module="org.wildfly.clustering.server">
                <transport lock-timeout="60000"/>
                <replicated-cache name="default">
                    <transaction mode="BATCH"/>
                </replicated-cache>
            </cache-container>
            <cache-container name="web" default-cache="repl" module="org.wildfly.clustering.web.infinispan">
                <transport lock-timeout="60000"/>
                <replicated-cache name="repl">
                    <locking isolation="REPEATABLE_READ"/>
                    <transaction mode="BATCH"/>
                    <file-store/>
                </replicated-cache>
                <distributed-cache name="dist">
                    <locking isolation="REPEATABLE_READ"/>
                    <transaction mode="BATCH"/>
                    <file-store/>
                </distributed-cache>
            </cache-container>
            <cache-container name="ejb" aliases="sfsb" default-cache="repl" module="org.wildfly.clustering.ejb.infinispan">
                <transport lock-timeout="60000"/>
                <replicated-cache name="repl">
                    <locking isolation="REPEATABLE_READ"/>
                    <object-memory size="10000"/>
                    <transaction mode="BATCH"/>
                    <file-store/>
                </replicated-cache>
                <distributed-cache name="dist">
                    <locking isolation="REPEATABLE_READ"/>
                    <transaction mode="BATCH"/>
                    <file-store/>
                </distributed-cache>
            </cache-container>
            <cache-container name="hibernate" module="org.infinispan.hibernate-cache">
                <transport lock-timeout="60000"/>
                <local-cache name="local-query">
                    <object-memory size="10000"/>
                    <expiration max-idle="100000"/>
                </local-cache>
                <invalidation-cache name="entity">
                    <transaction mode="NON_XA"/>
                    <object-memory size="10000"/>
                    <expiration max-idle="100000"/>
                </invalidation-cache>
                <replicated-cache name="timestamps"/>
            </cache-container>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:jaxrs:1.0"/>
        <subsystem xmlns="urn:jboss:domain:jca:5.0">
            <archive-validation enabled="true" fail-on-error="true" fail-on-warn="false"/>
            <bean-validation enabled="true"/>
            <default-workmanager>
                <short-running-threads>
                    <core-threads count="50"/>
                    <queue-length count="50"/>
                    <max-threads count="50"/>
                    <keepalive-time time="10" unit="seconds"/>
                </short-running-threads>
                <long-running-threads>
                    <core-threads count="50"/>
                    <queue-length count="50"/>
                    <max-threads count="50"/>
                    <keepalive-time time="10" unit="seconds"/>
                </long-running-threads>
            </default-workmanager>
            <cached-connection-manager/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:jgroups:7.0">
            <channels default="ee">
                <channel name="ee" stack="tcp" cluster="ejb"/>
            </channels>
            <stacks>
                <stack name="udp">
                    <transport type="UDP" socket-binding="jgroups-udp"/>
                    <protocol type="dns.DNS_PING" ><property name="dns_query">sso-ping</property><property name="async_discovery_use_separate_thread_per_request">true</property></protocol>
                    <protocol type="MERGE3"/>
                    <socket-protocol type="FD_SOCK" socket-binding="jgroups-udp-fd"/>
                    <protocol type="FD_ALL"/>
                    <protocol type="VERIFY_SUSPECT"/>
                    <protocol type="SYM_ENCRYPT"> <property name="provider">SunJCE</property> <property name="sym_algorithm">AES</property> <property name="encrypt_entire_message">true</property> <property name="keystore_name">/etc/jgroups-encrypt-secret-volume/jgroups.jceks</property> <property name="store_password">redhat</property> <property name="alias">secret-key</property> </protocol>
                    <protocol type="pbcast.NAKACK2"/>
                    <protocol type="UNICAST3"/>
                    <protocol type="pbcast.STABLE"/>
                    
 <auth-protocol type="AUTH">
 <digest-token algorithm="SHA-512">
 <shared-secret-reference clear-text="g4tiMLps"/>
 </digest-token>
 </auth-protocol>

                    <protocol type="pbcast.GMS"/>
                    <protocol type="UFC"/>
                    <protocol type="MFC"/>
                    <protocol type="FRAG3"/>
                </stack>
                <stack name="tcp">
                    <transport type="TCP" socket-binding="jgroups-tcp"/>
                    <protocol type="dns.DNS_PING" ><property name="dns_query">sso-ping</property><property name="async_discovery_use_separate_thread_per_request">true</property></protocol>
                    <protocol type="MERGE3"/>
                    <socket-protocol type="FD_SOCK" socket-binding="jgroups-tcp-fd"/>
                    <protocol type="FD_ALL"/>
                    <protocol type="VERIFY_SUSPECT"/>
                    <protocol type="SYM_ENCRYPT"> <property name="provider">SunJCE</property> <property name="sym_algorithm">AES</property> <property name="encrypt_entire_message">true</property> <property name="keystore_name">/etc/jgroups-encrypt-secret-volume/jgroups.jceks</property> <property name="store_password">redhat</property> <property name="alias">secret-key</property> </protocol>
                    <protocol type="pbcast.NAKACK2"/>
                    <protocol type="UNICAST3"/>
                    <protocol type="pbcast.STABLE"/>
                    
 <auth-protocol type="AUTH">
 <digest-token algorithm="SHA-512">
 <shared-secret-reference clear-text="g4tiMLps"/>
 </digest-token>
 </auth-protocol>

                    <protocol type="pbcast.GMS"/>
                    <protocol type="MFC"/>
                    <protocol type="FRAG3"/>
                </stack>
            </stacks>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:jmx:1.3">
            <expose-resolved-model/>
            <expose-expression-model/>
            <remoting-connector/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:jpa:1.1">
            <jpa default-datasource="" default-extended-persistence-inheritance="DEEP"/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:mail:3.0">
            <mail-session name="default" jndi-name="java:jboss/mail/Default">
                <smtp-server outbound-socket-binding-ref="mail-smtp"/>
            </mail-session>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:modcluster:5.0">
            <proxy name="default" advertise-socket="modcluster" listener="ajp">
                <dynamic-load-provider>
                    <load-metric type="cpu"/>
                </dynamic-load-provider>
            </proxy>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:naming:2.0">
            <remote-naming/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:remoting:4.0">
            <http-connector name="http-remoting-connector" connector-ref="default" security-realm="ApplicationRealm"/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:resource-adapters:4.0">
            <resource-adapters>
                <!-- ##RESOURCE_ADAPTERS## -->
            </resource-adapters>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:request-controller:1.0"/>
        <subsystem xmlns="urn:jboss:domain:security-manager:1.0">
            <deployment-permissions>
                <maximum-set>
                    <permission class="java.security.AllPermission"/>
                </maximum-set>
            </deployment-permissions>
        </subsystem>
        <subsystem xmlns="urn:wildfly:elytron:8.0" final-providers="combined-providers" disallowed-providers="OracleUcrypto">
            <providers>
                <aggregate-providers name="combined-providers">
                    <providers name="elytron"/>
                    <providers name="openssl"/>
                </aggregate-providers>
                <provider-loader name="elytron" module="org.wildfly.security.elytron"/>
                <provider-loader name="openssl" module="org.wildfly.openssl"/>
            </providers>
            <audit-logging>
                <file-audit-log name="local-audit" path="audit.log" relative-to="jboss.server.log.dir" format="JSON"/>
            </audit-logging>
            <security-domains>
                <security-domain name="ApplicationDomain" default-realm="ApplicationRealm" permission-mapper="default-permission-mapper">
                    <realm name="ApplicationRealm" role-decoder="groups-to-roles"/>
                    <realm name="local"/>
                </security-domain>
                <security-domain name="ManagementDomain" default-realm="ManagementRealm" permission-mapper="default-permission-mapper">
                    <realm name="ManagementRealm" role-decoder="groups-to-roles"/>
                    <realm name="local" role-mapper="super-user-mapper"/>
                </security-domain>
            </security-domains>
            <security-realms>
                <identity-realm name="local" identity="$local"/>
                <properties-realm name="ApplicationRealm">
                    <users-properties path="application-users.properties" relative-to="jboss.server.config.dir" digest-realm-name="ApplicationRealm"/>
                    <groups-properties path="application-roles.properties" relative-to="jboss.server.config.dir"/>
                </properties-realm>
                <properties-realm name="ManagementRealm">
                    <users-properties path="mgmt-users.properties" relative-to="jboss.server.config.dir" digest-realm-name="ManagementRealm"/>
                    <groups-properties path="mgmt-groups.properties" relative-to="jboss.server.config.dir"/>
                </properties-realm>
            </security-realms>
            <mappers>
                <simple-permission-mapper name="default-permission-mapper" mapping-mode="first">
                    <permission-mapping>
                        <principal name="anonymous"/>
                        <permission-set name="default-permissions"/>
                    </permission-mapping>
                    <permission-mapping match-all="true">
                        <permission-set name="login-permission"/>
                        <permission-set name="default-permissions"/>
                    </permission-mapping>
                </simple-permission-mapper>
                <constant-realm-mapper name="local" realm-name="local"/>
                <simple-role-decoder name="groups-to-roles" attribute="groups"/>
                <constant-role-mapper name="super-user-mapper">
                    <role name="SuperUser"/>
                </constant-role-mapper>
            </mappers>
            <permission-sets>
                <permission-set name="login-permission">
                    <permission class-name="org.wildfly.security.auth.permission.LoginPermission"/>
                </permission-set>
                <permission-set name="default-permissions">
                    <permission class-name="org.wildfly.extension.batch.jberet.deployment.BatchPermission" module="org.wildfly.extension.batch.jberet" target-name="*"/>
                    <permission class-name="org.wildfly.transaction.client.RemoteTransactionPermission" module="org.wildfly.transaction.client"/>
                    <permission class-name="org.jboss.ejb.client.RemoteEJBPermission" module="org.jboss.ejb-client"/>
                </permission-set>
            </permission-sets>
            <http>
                <http-authentication-factory name="management-http-authentication" security-domain="ManagementDomain" http-server-mechanism-factory="global">
                    <mechanism-configuration>
                        <mechanism mechanism-name="DIGEST">
                            <mechanism-realm realm-name="ManagementRealm"/>
                        </mechanism>
                    </mechanism-configuration>
                </http-authentication-factory>
                <provider-http-server-mechanism-factory name="global"/>
            </http>
            <sasl>
                <sasl-authentication-factory name="application-sasl-authentication" sasl-server-factory="configured" security-domain="ApplicationDomain">
                    <mechanism-configuration>
                        <mechanism mechanism-name="JBOSS-LOCAL-USER" realm-mapper="local"/>
                        <mechanism mechanism-name="DIGEST-MD5">
                            <mechanism-realm realm-name="ApplicationRealm"/>
                        </mechanism>
                    </mechanism-configuration>
                </sasl-authentication-factory>
                <sasl-authentication-factory name="management-sasl-authentication" sasl-server-factory="configured" security-domain="ManagementDomain">
                    <mechanism-configuration>
                        <mechanism mechanism-name="JBOSS-LOCAL-USER" realm-mapper="local"/>
                        <mechanism mechanism-name="DIGEST-MD5">
                            <mechanism-realm realm-name="ManagementRealm"/>
                        </mechanism>
                    </mechanism-configuration>
                </sasl-authentication-factory>
                <configurable-sasl-server-factory name="configured" sasl-server-factory="elytron">
                    <properties>
                        <property name="wildfly.sasl.local-user.default-user" value="$local"/>
                    </properties>
                </configurable-sasl-server-factory>
                <mechanism-provider-filtering-sasl-server-factory name="elytron" sasl-server-factory="global">
                    <filters>
                        <filter provider-name="WildFlyElytron"/>
                    </filters>
                </mechanism-provider-filtering-sasl-server-factory>
                <provider-sasl-server-factory name="global"/>
            </sasl>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:security:2.0">
            <!-- ##ELYTRON_INTEGRATION## -->
            <security-domains>
                <security-domain name="other" cache-type="default">
                    <authentication>
                        <login-module code="Remoting" flag="optional">
                            <module-option name="password-stacking" value="useFirstPass"/>
                        </login-module>
                        <login-module code="RealmDirect" flag="required">
                            <module-option name="password-stacking" value="useFirstPass"/>
                        </login-module>
                        <!-- ##OTHER_LOGIN_MODULES## -->
                    </authentication>
                </security-domain>
                <security-domain name="jboss-web-policy" cache-type="default">
                    <authorization>
                        <policy-module code="Delegating" flag="required"/>
                    </authorization>
                </security-domain>
                <security-domain name="jaspitest" cache-type="default">
                    <authentication-jaspi>
                        <login-module-stack name="dummy">
                            <login-module code="Dummy" flag="optional"/>
                        </login-module-stack>
                        <auth-module code="Dummy"/>
                    </authentication-jaspi>
                </security-domain>
                <security-domain name="jboss-ejb-policy" cache-type="default">
                    <authorization>
                        <policy-module code="Delegating" flag="required"/>
                    </authorization>
                </security-domain>
                <!-- no additional security domains configured --><!-- ##ADDITIONAL_SECURITY_DOMAINS## -->
            </security-domains>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:transactions:5.0">
            <core-environment node-identifier="${jboss.node.name}">
                <process-id>
                    <uuid/>
                </process-id>
            </core-environment>
            <recovery-environment socket-binding="txn-recovery-environment" status-socket-binding="txn-status-manager"/>
            <!-- ##JDBC_STORE## -->
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:weld:4.0"/>
        <subsystem xmlns="urn:wildfly:microprofile-config-smallrye:1.0"/>
        <subsystem xmlns="urn:wildfly:microprofile-health-smallrye:2.0" security-enabled="false" empty-liveness-checks-status="${env.MP_HEALTH_EMPTY_LIVENESS_CHECKS_STATUS:UP}" empty-readiness-checks-status="${env.MP_HEALTH_EMPTY_READINESS_CHECKS_STATUS:UP}"/>
        <subsystem xmlns="urn:wildfly:microprofile-metrics-smallrye:2.0" security-enabled="false" exposed-subsystems="*" prefix="${wildfly.metrics.prefix:wildfly}"/>
        <subsystem xmlns="urn:jboss:domain:undertow:10.0" default-server="default-server" default-virtual-host="default-host" default-servlet-container="default" default-security-domain="other">
            <buffer-cache name="default"/>
            <server name="default-server">
                <ajp-listener name="ajp" socket-binding="ajp"/>
                <http-listener name="default" socket-binding="http" redirect-socket="proxy-https" enable-http2="true" proxy-address-forwarding="true"/>
                <https-listener name="https" socket-binding="https" security-realm="ApplicationRealm" proxy-address-forwarding="true"/>
                <host name="default-host" alias="localhost">
                    <location name="/" handler="sso-welcome-content"/>
                    <!-- ##ACCESS_LOG_VALVE## -->
                    <http-invoker security-realm="ApplicationRealm"/>
                </host>
            </server>
            <servlet-container name="default">
                <jsp-config/>
                <websockets/>
            </servlet-container>
            <handlers>
                <file name="sso-welcome-content" path="${jboss.home.dir}/root-app-redirect"/>
            </handlers>
            <!-- ##HTTP_APPLICATION_SECURITY_DOMAINS## -->
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:keycloak-server:1.1">
            <web-context>auth</web-context>
            <providers>
                <provider>classpath:${jboss.home.dir}/providers/*</provider>
            </providers>
            <master-realm-name>master</master-realm-name>
            <scheduled-task-interval>900</scheduled-task-interval>
            <theme>
                <staticMaxAge>2592000</staticMaxAge>
                <cacheThemes>true</cacheThemes>
                <cacheTemplates>true</cacheTemplates>
                <dir>${jboss.home.dir}/themes</dir>
            </theme>
            <spi name="eventsStore">
                <provider name="jpa" enabled="true">
                    <properties>
                        <property name="exclude-events" value="[&quot;REFRESH_TOKEN&quot;]"/>
                    </properties>
                </provider>
            </spi>
            <spi name="userCache">
                <provider name="default" enabled="true"/>
            </spi>
            <spi name="userSessionPersister">
                <default-provider>jpa</default-provider>
            </spi>
            <spi name="timer">
                <default-provider>basic</default-provider>
            </spi>
            <spi name="connectionsHttpClient">
                <provider name="default" enabled="true"/>
            </spi>
            <spi name="connectionsJpa">
                <provider name="default" enabled="true">
                    <properties>
                        <property name="dataSource" value="java:jboss/datasources/KeycloakDS"/>
                        <property name="initializeEmpty" value="true"/>
                        <property name="migrationStrategy" value="update"/>
                        <property name="migrationExport" value="${jboss.home.dir}/keycloak-database-update.sql"/>
                    </properties>
                </provider>
            </spi>
            <spi name="realmCache">
                <provider name="default" enabled="true"/>
            </spi>
            <spi name="connectionsInfinispan">
                <default-provider>default</default-provider>
                <provider name="default" enabled="true">
                    <properties>
                        <property name="cacheContainer" value="java:jboss/infinispan/container/keycloak"/>
                    </properties>
                </provider>
            </spi>
            <spi name="jta-lookup">
                <default-provider>${keycloak.jta.lookup.provider:jboss}</default-provider>
                <provider name="jboss" enabled="true"/>
            </spi>
            <spi name="publicKeyStorage">
                <provider name="infinispan" enabled="true">
                    <properties>
                        <property name="minTimeBetweenRequests" value="10"/>
                    </properties>
                </provider>
            </spi>
            <spi name="x509cert-lookup">
                <default-provider>${keycloak.x509cert.lookup.provider:default}</default-provider>
                <provider name="default" enabled="true"/>
            </spi>
            <spi name="hostname"><default-provider>default</default-provider><provider name="default" enabled="true"><properties></properties></provider></spi>
            <spi name="truststore"><provider name="file" enabled="true"><properties><property name="file" value="/etc/sso-secret-volume/truststore.jks"/><property name="password" value="redhat"/><property name="hostname-verification-policy" value="WILDCARD"/><property name="disabled" value="false"/></properties></provider></spi>
            <!-- ##SSO_VAULT_CONFIG## -->
        </subsystem>
    </profile>
    <interfaces>
        <interface name="management">
            <inet-address value="${jboss.bind.address.management:127.0.0.1}"/>
        </interface>
        <interface name="public">
            <nic name="eth0"/>
        </interface>
        <interface name="private">
            <inet-address value="${jboss.bind.address.private:127.0.0.1}"/>
        </interface>
    </interfaces>
    <socket-binding-group name="standard-sockets" default-interface="public" port-offset="${jboss.socket.binding.port-offset:0}">
        <socket-binding name="ajp" port="${jboss.ajp.port:8009}"/>
        <socket-binding name="http" port="${jboss.http.port:8080}"/>
        <socket-binding name="https" port="${jboss.https.port:8443}"/>
        <socket-binding name="proxy-https" port="443"/>
        <socket-binding name="jgroups-mping" interface="private" multicast-address="${jboss.default.multicast.address:230.0.0.4}" multicast-port="45700"/>
        <socket-binding name="jgroups-tcp" interface="private" port="7600"/>
        <socket-binding name="jgroups-tcp-fd" interface="private" port="57600"/>
        <socket-binding name="jgroups-udp" interface="private" port="55200" multicast-address="${jboss.default.multicast.address:230.0.0.4}" multicast-port="45688"/>
        <socket-binding name="jgroups-udp-fd" interface="private" port="54200"/>
        <socket-binding name="management-http" interface="management" port="${jboss.management.http.port:9990}"/>
        <socket-binding name="management-https" interface="management" port="${jboss.management.https.port:9993}"/>
        <socket-binding name="modcluster" multicast-address="${jboss.modcluster.multicast.address:224.0.1.105}" multicast-port="23364"/>
        <socket-binding name="txn-recovery-environment" port="4712"/>
        <socket-binding name="txn-status-manager" port="4713"/>
        <outbound-socket-binding name="mail-smtp">
            <remote-destination host="localhost" port="25"/>
        </outbound-socket-binding>
    </socket-binding-group>
</server>
