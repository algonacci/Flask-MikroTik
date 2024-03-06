from flask import Flask, render_template, redirect, url_for, request, session
from helpers import connect_to_router, get_router_resources

app = Flask(__name__)

app.secret_key = 'your_secret_key'


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ip = request.form['ip']
        username = request.form['username']
        password = request.form['password']
        router_conn = connect_to_router(ip, username, password)
        if router_conn:
            session['logged_in'] = True
            session['username'] = username
            session['ip'] = ip
            session['password'] = password
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Failed to connect to the router. Please check your credentials and try again.")
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    ip = session.get('ip')
    username = session.get('username')
    password = session.get('password')

    router_data = get_router_resources(ip, username, password)

    uptime, free_memory, total_memory, free_hdd_space, total_hdd_space, router_os_version, cpu_frequency, cpu_cores, architecture, board_name, cpu_load, ram_percentage, hdd_percentage, cpu, used_hdd = router_data

    # Format the data into a more human-friendly format
    # Convert bytes to megabytes (MB) for display and round to two decimal places
    free_memory_mb = round(free_memory / (1024 ** 2), 2)
    total_memory_mb = round(total_memory / (1024 ** 2), 2)
    free_hdd_space_mb = round(free_hdd_space / (1024 ** 2), 2)
    total_hdd_space_mb = round(total_hdd_space / (1024 ** 2), 2)
    used_hdd_mb = round(used_hdd / (1024**2), 2)

    ram_percentage = round(ram_percentage, 2)
    hdd_percentage = round(hdd_percentage, 2)

    return render_template('dashboard.html',
                           uptime=uptime,
                           free_memory=free_memory_mb,
                           total_memory=total_memory_mb,
                           router_os_version=router_os_version,
                           cpu_frequency=cpu_frequency,
                           cpu_cores=cpu_cores,
                           architecture=architecture,
                           board_name=board_name,
                           cpu_load=cpu_load,
                           ram_percentage=ram_percentage,
                           hdd_percentage=hdd_percentage,
                           free_hdd_space=free_hdd_space_mb,
                           total_hdd_space=total_hdd_space_mb,
                           cpu=cpu,
                           used_hdd=used_hdd_mb)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
