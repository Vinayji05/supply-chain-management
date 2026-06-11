#include <bits/stdc++.h>
using namespace std;

// Simple Dijkstra-based simulator input format:
// First line: N M
// Next M lines: u v cost  (1-based nodes)
// Last line: source target

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    if(!(cin >> N >> M)) return 0;
    vector<vector<pair<int,int>>> g(N+1);
    for(int i=0;i<M;i++){int u,v,w; cin>>u>>v>>w; g[u].push_back({v,w}); g[v].push_back({u,w});}
    int s,t; cin>>s>>t;
    const long long INF = (1LL<<60);
    vector<long long> dist(N+1, INF);
    vector<int> prev(N+1, -1);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
    dist[s]=0; pq.push({0,s});
    while(!pq.empty()){
        auto p = pq.top(); pq.pop();
        long long d = p.first; int u = p.second;
        if(d!=dist[u]) continue;
        if(u==t) break;
        for(auto &vw: g[u]){
            int v = vw.first; int w = vw.second;
            if(dist[v]>d+w){ dist[v]=d+w; prev[v]=u; pq.push({dist[v], v}); }
        }
    }
    vector<int> path;
    if(dist[t]==INF){
        cout << "{\"cost\": null, \"path\": []}\n";
        return 0;
    }
    for(int cur=t; cur!=-1; cur=prev[cur]) path.push_back(cur);
    reverse(path.begin(), path.end());
    // Output minimal JSON
    cout << "{\"cost\": " << dist[t] << ", \"path\": [";
    for(size_t i=0;i<path.size();++i){ if(i) cout<<", "; cout<<path[i]; }
    cout << "]}\n";
    return 0;
}
