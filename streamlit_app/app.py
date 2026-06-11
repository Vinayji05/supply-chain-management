import streamlit as st
import subprocess
import json
import tempfile
import os
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except Exception:
    MYSQL_AVAILABLE = False

st.title('Supply Chain Management Simulator')

uploaded = st.file_uploader('Upload graph file (format: N M; M lines u v cost; last line: s t)', type=['txt','csv'])
if uploaded is not None:
    data = uploaded.read().decode('utf-8')
    with open('graph_input.txt','w',encoding='utf-8') as f:
        f.write(data)
    st.success('Saved graph_input.txt')

col1, col2 = st.columns(2)
with col1:
    src = st.number_input('Source node', min_value=1, value=1, step=1)
with col2:
    tgt = st.number_input('Target node', min_value=1, value=1, step=1)

exe_path = st.text_input('Path to simulator executable', value=os.path.abspath('src\\simulator\\simulate.exe'))

if st.button('Run simulation'):
    # Ensure an input exists
    if os.path.exists('graph_input.txt'):
        # Append source/target line if not present
        with open('graph_input.txt','r',encoding='utf-8') as f: lines = f.read().strip().splitlines()
        # If last line contains two ints, replace them; else append
        try:
            last = lines[-1].strip().split()
            if len(last)==2:
                lines[-1] = f"{src} {tgt}"
            else:
                lines.append(f"{src} {tgt}")
        except Exception:
            lines.append(f"{src} {tgt}")
        with open('graph_input.txt','w',encoding='utf-8') as f: f.write('\n'.join(lines)+'\n')

        # Run simulator
        try:
            res = subprocess.run([exe_path], input=open('graph_input.txt','rb').read(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode!=0:
                st.error('Simulator failed: ' + res.stderr.decode('utf-8',errors='ignore'))
            else:
                out = res.stdout.decode('utf-8')
                st.code(out)
                try:
                    j = json.loads(out)
                    st.write('Cost:', j.get('cost'))
                    st.write('Path:', j.get('path'))
                    if MYSQL_AVAILABLE and st.checkbox('Save to MySQL'):
                        host = st.text_input('MySQL host', value='localhost')
                        user = st.text_input('MySQL user', value='root')
                        password = st.text_input('MySQL password', type='password')
                        database = st.text_input('DB name', value='scm')
                        if st.button('Save now'):
                            conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
                            cur = conn.cursor()
                            cur.execute("INSERT INTO simulation_results (source,target,cost,path) VALUES (%s,%s,%s,%s)", (src,tgt,str(j.get('cost')), json.dumps(j.get('path'))))
                            conn.commit()
                            conn.close()
                            st.success('Saved')
                except Exception as e:
                    st.warning('Could not parse output as JSON: ' + str(e))
        except FileNotFoundError:
            st.error('Simulator executable not found at path: ' + exe_path)
    else:
        st.error('No graph_input.txt found. Upload a graph first.')
