from librouteros import connect


def connect_to_router(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD):
    try:
        conn = connect(host=ROUTER_IP,
                       username=ROUTER_USERNAME,
                       password=ROUTER_PASSWORD)
        return conn
    except Exception as e:
        return None


def get_router_resources(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD):
    conn = connect_to_router(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD)
    if conn:
        try:
            response = conn(cmd='/system/resource/print')
            items = list(response)
            if items:
                resource = items[0]
                uptime = resource.get('uptime')
                free_memory = resource.get('free-memory')
                total_memory = resource.get('total-memory')
                free_hdd_space = resource.get('free-hdd-space')
                total_hdd_space = resource.get('total-hdd-space')
                cpu = resource.get('cpu')
                cpu_load = resource.get('cpu-load')
                router_os_version = resource.get('version')
                cpu_frequency = resource.get('cpu-frequency')
                cpu_cores = resource.get('cpu-count')
                architecture = resource.get('architecture-name')
                board_name = resource.get('board-name')

                ram_percentage = 100 - ((free_memory / total_memory) * 100)
                hdd_percentage = 100 - \
                    ((free_hdd_space / total_hdd_space) * 100)

                used_hdd = total_hdd_space - free_hdd_space
            else:
                return "No data received"
            conn.close()
            return (uptime, free_memory, total_memory, free_hdd_space, total_hdd_space, router_os_version, cpu_frequency, cpu_cores,
                    architecture, board_name, cpu_load, ram_percentage, hdd_percentage, cpu, used_hdd)

        except Exception as e:
            conn.close()
            return (str(e),) * 15
    else:
        return ("Failed to connect to the router.",) * 15
