# Описание моделей технической архитектуры

В этом документе представлено описание моделей технической архитектуры из каталогов `@_metamodel_/iaas/cloud.ru/advanced/entities/**` и `@_metamodel_/seaf-core/entities/ta/**`.

| папка(короткое имя) | название сущности | свойство (название как в сущности и в скобках расшифровка) | тип свойства (строка, массив и т.д. ) | ссылка на какую сущность с этого свойства если есть | сопоставление моделей между собой |
|---|---|---|---|---|---|
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | id (Идентификатор политики РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | name (Название политики РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_type (Назначение политики РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | enabled (Статус политики РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_definition.max_backups (Кол-во хранимых РК (-1 безлимит)) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_definition.retention_duration_days (Срок хранения РК (дней, -1 безлимит)) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_definition.day_backups (Кол-во хранимых daily РК) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_definition.week_backups (Кол-во хранимых weekly РК) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_definition.month_backups (Кол-во хранимых monthly РК) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_definition.year_backups (Кол-во хранимых yearly РК) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | operation_definition.timezone (Часовой пояс) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | trigger.id (ID расписания РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | trigger.name (Название расписания РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | trigger.type (Тип расписания РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | trigger.properties.pattern (Расписание РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | trigger.properties.start_time (Дата начала РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | associated_vaults (Привязанные хранилища РК) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.backup_policies | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | id (CCE ID) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | name (Наименование кластера) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | alias (Alias кластера) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | flavor (Flavor кластера) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | version (Версия CCE) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | platform_version (Версия платформы CCE) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | vpc_id (Идентификатор VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | subnet_id (Идентификатор подсети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | addresses (IP адреса) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | security_groups (Группы безопасности) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | container_network (Сеть POD'ов) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | service_network (Сеть сервисов) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | authentication (Тип аутентификации) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | masters_az (Зоны доступности) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | supportistio (Поддержка istio) | boolean | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | endpoints.url (URL эндпоинта) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | endpoints.type (Тип эндпоинта) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.cces | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | id (Идентификатор сервиса DMS) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | name (Наименование сервиса DMS) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | engine (Движок сервиса DMS (rabbit или kafka)) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | engine_version (Версия движка сервиса DMS) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | port (Порт сервиса) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | address (IP адрес сервиса DMS) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | vpc_id (Идентификатор VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | subnet_id (Идентификатор подсети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | status (Статус сервиса DMS) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | type (Тип отказоустойчивости DMS) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | specification (Спецификация) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | security_groups (Группы безопасности) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | available_az (Зоны доступности) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | storage_space (Доступное место) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | total_storage_space (Размер хранилища) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | used_storage_space (Хранилище использовано) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | storage_spec_code (Спецификация хранилища) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | management (URL мэнеджмент интерфейса) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | support_features (ПОддерживаемые фичи) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | node_num (Количество экземпляров) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | disk_encrypted (Шифрование диска) | boolean | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.dmss | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | id (Идентификатор ВМ) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | name (Наименование сервера) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | description (Описание) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | flavor (Спецификация (Flavor)) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | status (Статус) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | az (Зона доступности) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | os.bit (Разрядность ОС) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | os.type (ОС) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | nic_qty (Количество сетевых адаптеров) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | addresses (IP адреса) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | vpc_id (VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | subnets (Subnet) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | ram (ОЗУ) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | cpu.cores (Ядра) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | cpu.frequency (Частота) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | security_groups (Группы безопасности) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | tags (Тэги) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | disks (Диски) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | type (Тип сервера) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.ecss | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | id (Идентификатор EIP) | | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | ext_address (Внешний адрес) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | int_address (Внутренний адрес) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | type (Тип адреса) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | port_id (Идентификатор порта для которого привязан IP) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | limit.rule_id (ID правила) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | limit.rule_name (Название правила) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | limit.throughput (Пропускная способность (Mbps)) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | limit.type (Тип лимита) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.eips | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | id (ELB ID) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | name (Наименование Elastic Load Balancer) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | description (Описание ELB) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | subnet_id (Идентификатор подсети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | port_id (Идентификатор порта) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | operating_status (Статус ELB (Online или Offline)) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | provisioning_status (Статус ELB (включен или выключен)) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | address (Внутренний IP адрес) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | listeners (LB Listeners) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | pools (Пулы балансировки) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | tags (Тэги) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.elbs | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | id (Id Nat Gateway) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | name (Наименование Nat Gateway) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | description (Описание хранилища РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | subnet_id (Идентификатор подсети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | status (Статус шлюза) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | address (Внутренний IP адрес) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | snat_rules (Правила SNAT) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | dnat_rules (Правила DNAT) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.nat_gateways | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | id (Идентификатор пиринга) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | name (Название пиринга) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | request_vpc (Источник VPC ID) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | accept_vpc (Назначение VPC ID) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | description (Описание) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | status (Состояние) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.peerings | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | id (Идентификатор RDS) | | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | name (Наименование БД) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | description (Описание) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | flavor (Спецификация (Flavor)) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | az (Зона доступности) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | status (Статус БД) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | private_ips (Внутренние IP адреса) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | public_ips (Внешние IP адреса) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | vpc_id (VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | subnet_id (VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | tags (Тэги) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | volume.type (Тип диска) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | volume.size (Размер (ГБ)) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | nodes (Ноды СУБД) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | switch_strategy (Метод переключения) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | backup_strategy.start_time (Начало задания) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | backup_strategy.keep_days (Длительность хранения (дней)) | integer | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | type (Тип БД) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.rdss | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.security_groups | id (Security Groups ID) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.security_groups | name (Security Group Name) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.security_groups | description (Описание Security Group) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.security_groups | rules (Endpoints) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.security_groups | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.security_groups | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | id (ID Подсети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | cidr (CIDR сети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | description (Описание) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | name (Название подсети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | gateway (Название VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | vpc (ID VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | dns_list (DNS сервера) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.subnets | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vaults | id (ID хранилища РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vaults | name (Наименование хранилища РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vaults | description (Описание хранилища РК) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vaults | resources (Ресурсы РК) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vaults | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vaults | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpcs | id (Идентификатор VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpcs | cidr (CIDR сети) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpcs | description (Описание) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpcs | name (Название VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpcs | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpcs | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | id (Идентификатор VPN соединения) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | name (Название соединения) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | gw_id (ID of local VPN Gateway) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | remote_gw_ip (IP адрес удаленного узла) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | remote_subnets (CIDR удаленных сетей) | array | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | branch_id (ID офиса или ЦОД) | | seaf.ta.services.office, seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_connections | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | id (Идентификатор VPN Gateway) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | name (Название объекта) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | vpc_id (VPC) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | subnet_id (Subnet) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | ip_address (Адрес) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | type (Протокол) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | tenant (Тенант в облаке) | string | | |
| advanced | seaf.ta.reverse.cloud_ru.advanced.vpn_gateways | DC (Датацентр/IaaS провайдер) | | seaf.ta.services.dc | |
| ta | seaf.ta.components.hw_storage | vendor (Производитель и модель) | string | | |
| ta | seaf.ta.components.hw_storage | volume (Общий объём хранилища в ТБ) | integer | | |
| ta | seaf.ta.components.hw_storage | disk_type (Тип используемых дисков) | string | | |
| ta | seaf.ta.components.hw_storage | protocols (Поддерживаемые протоколы для клиентских подключений) | string | | |
| ta | seaf.ta.components.hw_storage | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.components.hw_storage | sw_storage_connected (К каким техническим сервисам СХД подключено) | array | seaf.ta.services.storage | |
| ta | seaf.ta.components.hw_storage | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.components.k8s_deployment | namespace_ref (Ссылка на namespace) | | seaf.ta.components.k8s_namespace | |
| ta | seaf.ta.components.k8s_deployment | cluster_ref (Ссылка на кластер) | | seaf.ta.services.k8s | |
| ta | seaf.ta.components.k8s_deployment | labels (Список labels) | array | | |
| ta | seaf.ta.components.k8s_deployment | containers.name (название контейнера) | string | | |
| ta | seaf.ta.components.k8s_deployment | containers.image (ссылка на образ) | string | | |
| ta | seaf.ta.components.k8s_deployment | containers.resources.limits.cpu (ограничения на процессор) | string | | |
| ta | seaf.ta.components.k8s_deployment | containers.resources.limits.ram (ограничения на оперативную память) | string | | |
| ta | seaf.ta.components.k8s_hpa | cluster_ref (Ссылка на кластер) | | seaf.ta.services.k8s | |
| ta | seaf.ta.components.k8s_hpa | min (минимальное количество реплик) | integer | | |
| ta | seaf.ta.components.k8s_hpa | max (максимальное количество реплик) | integer | | |
| ta | seaf.ta.components.k8s_hpa | target_ref (объект автомасштабирования) | | seaf.ta.components.k8s_deployment | |
| ta | seaf.ta.components.k8s_namespace | cluster_ref (Ссылка на кластер) | | seaf.ta.services.k8s | |
| ta | seaf.ta.components.k8s_namespace | labels (Список labels) | array | | |
| ta | seaf.ta.components.k8s_node | version (Версия kubelet) | string | | |
| ta | seaf.ta.components.k8s_node | architecture (Архитектура CPU) | string | | |
| ta | seaf.ta.components.k8s_node | cpu (Количество CPU для ноды) | integer | | |
| ta | seaf.ta.components.k8s_node | ram (Количество RAM для ноды, GB) | integer | | |
| ta | seaf.ta.components.k8s_node | cluster_ref (Кластер Kubernetes) | | seaf.ta.services.k8s | |
| ta | seaf.ta.components.k8s_node | zone (Название зона доступнности, в которой расположена нода) | string | | |
| ta | seaf.ta.components.k8s_node | labels (Метки) | array | | |
| ta | seaf.ta.components.network | model (Модель и производитель) | string | | |
| ta | seaf.ta.components.network | realization_type (Тип исполнения) | string | | |
| ta | seaf.ta.components.network | type (Тип устройства) | string | | |
| ta | seaf.ta.components.network | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.components.network | network_connection_devices (Перечисление связанных сетевых линков) | array | seaf.ta.services.network_links | |
| ta | seaf.ta.components.network | purpose (Функциональное назначение сетевого аплаенса) | string | | |
| ta | seaf.ta.components.network | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.components.network | address (IP адрес устройства) | string | | |
| ta | seaf.ta.components.network | segment (Вхождение в сетевые сегменты сети) | | seaf.ta.services.network_segment | |
| ta | seaf.ta.components.network | is_part_of_IS_service (Перечисление связанных КБ сервисов) | array | seaf.ta.services.kb | |
| ta | seaf.ta.components.server | type (Тип) | string | | |
| ta | seaf.ta.components.server | fqdn (Имя сервера FQDN) | string | | |
| ta | seaf.ta.components.server | os.type (Тип ОС) | string | | |
| ta | seaf.ta.components.server | os.bit (Битность ОС) | string | | |
| ta | seaf.ta.components.server | cpu.cores (Ядра) | integer | | |
| ta | seaf.ta.components.server | cpu.frequency (Частота) | integer | | |
| ta | seaf.ta.components.server | ram (Количество RAM, GB) | integer | | |
| ta | seaf.ta.components.server | gpu (Графические процессоры) | array | | |
| ta | seaf.ta.components.server | disks (Диски) | array | | |
| ta | seaf.ta.components.server | nic_qty (Количество NIC) | integer | | |
| ta | seaf.ta.components.server | az (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.components.server | virtualization (Кластер виртуализации) | | seaf.ta.services.cluster_virtualization | |
| ta | seaf.ta.components.server | subnets (Подсети) | array | seaf.ta.services.network | |
| ta | seaf.ta.components.server | is_part_of_compute_service (Какие сервисы вычислений реализует) | array | seaf.ta.services.compute_service | |
| ta | seaf.ta.components.server | is_part_of_cluster_virtualization (Какие кластеры виртуализации реализует) | array | seaf.ta.services.cluster_virtualization | |
| ta | seaf.ta.components.server | is_part_of_k8s_cluster (Какие кластеры Kubernetes реализует) | array | seaf.ta.services.k8s | |
| ta | seaf.ta.components.server | is_part_of_cluster (Какие кластеры вычислений реализует) | array | seaf.ta.services.cluster | |
| ta | seaf.ta.components.server | is_monitoring_connected (Какие технические сервисы мониторинга реализует (т.е. является узлом хранения или управления)) | array | seaf.ta.services.monitoring | |
| ta | seaf.ta.components.server | is_backup_connected (Какие технические сервисы резервного копирования реализует (т.е. является узлом хранения или управления)) | array | seaf.ta.services.backup | |
| ta | seaf.ta.components.server | sw_storage_connected (Какие технические сервисы СХД реализует (т.е. является узлом хранения или управления в составе SDS)) | array | seaf.ta.services.storage | |
| ta | seaf.ta.components.server | software (Какое ПО и лицезии установлены) | array | seaf.ta.services.software | |
| ta | seaf.ta.components.server | vendor (Производитель) | string | | |
| ta | seaf.ta.components.server | model (Модель) | string | | |
| ta | seaf.ta.components.server | storage (Подключенные СХД) | array | seaf.ta.components.hw_storage | |
| ta | seaf.ta.components.server | vlan (Подключенные VLAN) | array | | |
| ta | seaf.ta.components.server | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.components.user_device | device_type (Тип устройства) | string | | |
| ta | seaf.ta.components.user_device | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.components.user_device | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.components.user_device | segment (Вхождение в сетевые сегменты сети) | | seaf.ta.services.network_segment | |
| ta | seaf.ta.components.user_device | network_connection_devices (Перечисление связанных сетевых линков) | array | seaf.ta.services.network_links | |
| ta | seaf.ta.services.environment | | | | |
| ta | seaf.ta.services.stand | env (В какое окружение входит стенд) | | seaf.ta.services.environment | |
| ta | seaf.ta.services.backup | availabilityzone (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.backup | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.backup | path (Место хранения РК) | string | | |
| ta | seaf.ta.services.backup | replication (Репликация в другой ЦОД) | boolean | | |
| ta | seaf.ta.services.backup | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.cluster | availabilityzone (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.cluster | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.cluster | fqdn (FQDN имя кластера) | string | | |
| ta | seaf.ta.services.cluster | reservation_type (Тип резервирования кластера) | string | | |
| ta | seaf.ta.services.cluster | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.cluster | service_type (Тип сервиса) | string | | |
| ta | seaf.ta.services.cluster_virtualization | hypervisor (Гипервизор) | string | | |
| ta | seaf.ta.services.cluster_virtualization | oversubscription_rate (Коэффициент переподписки кластера виртуализации) | integer | | |
| ta | seaf.ta.services.cluster_virtualization | drs_support (Поддержка DRS кластером виртуализации) | boolean | | |
| ta | seaf.ta.services.cluster_virtualization | sdrs_support (Поддержка Storage DRS кластером виртуализации) | boolean | | |
| ta | seaf.ta.services.cluster_virtualization | availabilityzone (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.cluster_virtualization | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.cluster_virtualization | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.compute_service | availabilityzone (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.compute_service | service_type (Тип сервиса) | string | | |
| ta | seaf.ta.services.compute_service | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.compute_service | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.dc | ownership (Тип владения ЦОД) | string | | |
| ta | seaf.ta.services.dc | type (Тип ЦОД) | string | | |
| ta | seaf.ta.services.dc | vendor (Поставщик) | string | | |
| ta | seaf.ta.services.dc | address (Адрес ЦОД) | string | | |
| ta | seaf.ta.services.dc | rack_qty (Количество стоек (аренда или владение)) | integer | | |
| ta | seaf.ta.services.dc | tier (Уровень сертификации ЦОД) | string | | |
| ta | seaf.ta.services.dc | availabilityzone (В какую зону доступности входит DC) | | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.dc_az | vendor (Поставщик) | string | | |
| ta | seaf.ta.services.dc_az | region (В какой регион входит зона доступности) | | seaf.ta.services.dc_region | |
| ta | seaf.ta.services.dc_region | | | | |
| ta | seaf.ta.services.k8s | fqdn (FQDN кластера k8s) | string | | |
| ta | seaf.ta.services.k8s | availabilityzone (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.k8s | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.k8s | is_own (Кластер куплен как услуга) | boolean | | |
| ta | seaf.ta.services.k8s | software (ПО реализующее Kubernetes кластер) | string | | |
| ta | seaf.ta.services.k8s | cni (CNI плагин) | string | | |
| ta | seaf.ta.services.k8s | service_mesh (Service Mesh) | string | | |
| ta | seaf.ta.services.k8s | cluster_autoscaler (Работа автомасштабирования воркер нод кластера) | boolean | | |
| ta | seaf.ta.services.k8s | keys (Хранилище секретов кластера) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | idm (Сервис управления учетными записями (IdM)) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | policy (ПО для реализации управления политиками) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | auth (ПО для реализации внешней системой аутентификации) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | pam (Сервис управления привилегированным доступом (PAM)) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | ca (Центр управления сертификатами (CMC)) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | audit (Сервис аудита/журналирования (SIEM/Log)) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | audit_policy (Политика аудита (логов)) | string | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | monitoring (Сервисы мониторинга/журналирования) | array | seaf.ta.services.monitoring | |
| ta | seaf.ta.services.k8s | backup (Сервисы резервного копирования) | array | seaf.ta.services.backup | |
| ta | seaf.ta.services.k8s | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.k8s | registries (Разрешенные реестры/репозитории ПО) | array | seaf.ta.services.kb | |
| ta | seaf.ta.services.k8s | management_networks (Управляющие сети (Management)) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.kb | technology (Технология) | string | | |
| ta | seaf.ta.services.kb | software_name (Продукт) | string | | |
| ta | seaf.ta.services.kb | tag (Тег) | string | | |
| ta | seaf.ta.services.kb | status (Статус) | string | | |
| ta | seaf.ta.services.kb | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.logical_link | source (Источник связи) | | seaf.ta.components.hw_storage, seaf.ta.components.network, seaf.ta.components.server, seaf.ta.components.user_device, seaf.ta.services.backup, seaf.ta.services.cluster, seaf.ta.services.cluster_virtualization, seaf.ta.services.compute_service, seaf.ta.services.dc, seaf.ta.services.dc_az, seaf.ta.services.dc_region, seaf.ta.services.k8s, seaf.ta.services.kb, seaf.ta.services.monitoring, seaf.ta.services.network, seaf.ta.services.network_links, seaf.ta.services.network_segment, seaf.ta.services.office, seaf.ta.services.software, seaf.ta.services.storage | |
| ta | seaf.ta.services.logical_link | target (Приемник связи) | array | seaf.ta.components.hw_storage, seaf.ta.components.network, seaf.ta.components.server, seaf.ta.components.user_device, seaf.ta.services.backup, seaf.ta.services.cluster, seaf.ta.services.cluster_virtualization, seaf.ta.services.compute_service, seaf.ta.services.dc, seaf.ta.services.dc_az, seaf.ta.services.dc_region, seaf.ta.services.k8s, seaf.ta.services.kb, seaf.ta.services.monitoring, seaf.ta.services.network, seaf.ta.services.network_links, seaf.ta.services.network_segment, seaf.ta.services.office, seaf.ta.services.software, seaf.ta.services.storage | |
| ta | seaf.ta.services.logical_link | direction (Направление связи) | string | | |
| ta | seaf.ta.services.monitoring | availabilityzone (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.monitoring | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.monitoring | name (Производитель и название системы мониторинга) | string | | |
| ta | seaf.ta.services.monitoring | role (Роль) | array | | |
| ta | seaf.ta.services.monitoring | ha (Высокая доступность системы мониторинга) | boolean | | |
| ta | seaf.ta.services.monitoring | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.network | type (Тип) | string | | |
| ta | seaf.ta.services.network | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.network | wan_ip (Внешняя сеть\IP) | string | | |
| ta | seaf.ta.services.network | provider (Оператор связи) | string | | |
| ta | seaf.ta.services.network | segment (Вхождение в сетевые сегменты сети) | array | seaf.ta.services.network_segment | |
| ta | seaf.ta.services.network | VRF (VRF) | string | | |
| ta | seaf.ta.services.network | autonomus_system (Автономная система) | string | | |
| ta | seaf.ta.services.network | ip_version (Версия IP) | string | | |
| ta | seaf.ta.services.network | lan_type (Тип LAN) | string | | |
| ta | seaf.ta.services.network | vlan (Имя виртуальной сети (VLAN)) | integer | | |
| ta | seaf.ta.services.network | ipnetwork (IP-сеть и маска) | string | | |
| ta | seaf.ta.services.network | purpose (Назначение) | string | | |
| ta | seaf.ta.services.network_links | network_connection (Перечисление связей) | array | seaf.ta.services.network, seaf.ta.components.network | |
| ta | seaf.ta.services.network_links | typeL1 (Протокол сигнального уровня (L1)) | string | | |
| ta | seaf.ta.services.network_links | typeL2 (Проткол канального уровня (L2)) | string | | |
| ta | seaf.ta.services.network_links | routing (Протокол маршрутизации) | string | | |
| ta | seaf.ta.services.network_links | encryption (Тип шифрования канала) | string | | |
| ta | seaf.ta.services.network_links | encapsulation (Инкапсуляция и туннелирвоание) | string | | |
| ta | seaf.ta.services.network_links | technology (Технология коммуникации) | string | | |
| ta | seaf.ta.services.network_links | sla (Тип SLA) | string | | |
| ta | seaf.ta.services.network_segment | | | | |
| ta | seaf.ta.services.office | address (Адрес офиса или местоположения) | string | | |
| ta | seaf.ta.services.office | region (В какой регион входит офис) | | seaf.ta.services.dc_region | |
| ta | seaf.ta.services.software | vendor (Производитель ПО) | string | | |
| ta | seaf.ta.services.software | type (Тип лицензии) | string | | |
| ta | seaf.ta.services.software | support (Наличие платной поддержки вендора\интегратора) | string | | |
| ta | seaf.ta.services.software | expiration (Срок действия лицензий) | string | | |
| ta | seaf.ta.services.software | lic_qty (Количество лицензий) | integer | | |
| ta | seaf.ta.services.storage | type (Тип) | string | | |
| ta | seaf.ta.services.storage | software (ПО реализующее SDS) | string | | |
| ta | seaf.ta.services.storage | volume (Общий объём хранилища в ТБ) | integer | | |
| ta | seaf.ta.services.storage | disk_type (Тип используемых дисков) | string | | |
| ta | seaf.ta.services.storage | erasure_coding (Параметр чётности) | integer | | |
| ta | seaf.ta.services.storage | protocols (Поддерживаемые протоколы для клиентских подключений) | string | | |
| ta | seaf.ta.services.storage | availabilityzone (В какие зоны доступности входит) | array | seaf.ta.services.dc_az | |
| ta | seaf.ta.services.storage | location (ID ЦОД или Офиса) | array | seaf.ta.services.dc, seaf.ta.services.office | |
| ta | seaf.ta.services.storage | network_connection (Перечисление связанных сетей) | array | seaf.ta.services.network | |
| ta | seaf.ta.services.storage | sla (SLA хранилища) | integer | | |
| ta | seaf.ta.services.storage | hw_storage_connected (Какие СХД подключены) | array | seaf.ta.components.hw_storage | |
