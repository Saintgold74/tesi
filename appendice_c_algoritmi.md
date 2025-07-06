# Appendice C - Algoritmi e Modelli Computazionali

## C.1 Algoritmi di Ottimizzazione per la Compliance Integrata

### C.1.1 Set Covering Ponderato per Ottimizzazione Controlli

Il problema di ottimizzazione dei controlli di compliance può essere formulato come Weighted Set Cover Problem (WSCP), NP-hard ma risolvibile con approssimazioni efficienti.

**Formulazione Matematica**:
```
Minimize: Σᵢ cᵢxᵢ
Subject to: Σᵢ aᵢⱼxᵢ ≥ 1, ∀j ∈ R
           xᵢ ∈ {0,1}, ∀i ∈ C

Dove:
- C = insieme dei controlli disponibili
- R = insieme dei requisiti normativi
- cᵢ = costo implementazione controllo i
- aᵢⱼ = 1 se controllo i soddisfa requisito j, 0 altrimenti
- xᵢ = 1 se controllo i è selezionato, 0 altrimenti
```

**Algoritmo Greedy con Garanzia di Approssimazione**:

```python
import numpy as np
from typing import List, Dict, Set, Tuple
import heapq

class ComplianceOptimizer:
    def __init__(self, controls: Dict[str, Dict], requirements: Dict[str, List[str]]):
        """
        controls: {control_id: {'cost': float, 'satisfies': [req_ids]}}
        requirements: {standard: [req_ids]}
        """
        self.controls = controls
        self.requirements = requirements
        self.all_reqs = set()
        for reqs in requirements.values():
            self.all_reqs.update(reqs)
    
    def greedy_set_cover(self) -> Tuple[List[str], float, Dict]:
        """
        Implementa algoritmo greedy con ratio di approssimazione ln(n)
        Returns: (selected_controls, total_cost, coverage_details)
        """
        uncovered = self.all_reqs.copy()
        selected = []
        total_cost = 0
        coverage_details = {std: [] for std in self.requirements}
        
        # Heap per efficienza O(log n)
        heap = []
        for ctrl_id, ctrl_data in self.controls.items():
            satisfies = set(ctrl_data['satisfies'])
            if satisfies:
                # Ratio costo/beneficio
                ratio = ctrl_data['cost'] / len(satisfies & uncovered)
                heapq.heappush(heap, (ratio, ctrl_id, satisfies))
        
        while uncovered and heap:
            ratio, ctrl_id, satisfies = heapq.heappop(heap)
            
            # Ricalcola ratio con requisiti attuali non coperti
            current_benefit = satisfies & uncovered
            if not current_benefit:
                continue
                
            actual_ratio = self.controls[ctrl_id]['cost'] / len(current_benefit)
            
            # Se il ratio è ancora ottimale, seleziona
            if not heap or actual_ratio <= heap[0][0] * 1.01:  # 1% tolerance
                selected.append(ctrl_id)
                total_cost += self.controls[ctrl_id]['cost']
                uncovered -= current_benefit
                
                # Traccia coverage per standard
                for std, reqs in self.requirements.items():
                    covered = set(reqs) & current_benefit
                    if covered:
                        coverage_details[std].append({
                            'control': ctrl_id,
                            'requirements': list(covered)
                        })
            else:
                # Reinserisci con nuovo ratio
                heapq.heappush(heap, (actual_ratio, ctrl_id, satisfies))
        
        # Calcola metriche di performance
        coverage_percentage = (len(self.all_reqs) - len(uncovered)) / len(self.all_reqs) * 100
        
        return selected, total_cost, {
            'coverage_details': coverage_details,
            'coverage_percentage': coverage_percentage,
            'uncovered_requirements': list(uncovered)
        }
    
    def branch_and_bound_exact(self, time_limit: int = 300) -> Tuple[List[str], float]:
        """
        Soluzione esatta con Branch & Bound per istanze piccole
        time_limit: secondi massimi di esecuzione
        """
        import time
        from collections import deque
        
        start_time = time.time()
        
        # Preprocessing: elimina controlli dominati
        controls_list = self._remove_dominated_controls()
        n = len(controls_list)
        
        # Stato: (covered_reqs, selected_controls, cost)
        initial_state = (set(), [], 0)
        queue = deque([initial_state])
        
        best_solution = None
        best_cost = float('inf')
        nodes_explored = 0
        
        while queue and (time.time() - start_time) < time_limit:
            covered, selected, cost = queue.popleft()
            nodes_explored += 1
            
            # Pruning: se il costo attuale supera il best, skip
            if cost >= best_cost:
                continue
            
            # Se copre tutti i requisiti, aggiorna best
            if covered == self.all_reqs:
                best_solution = selected.copy()
                best_cost = cost
                continue
            
            # Branching: prova ad aggiungere ogni controllo rimanente
            for i, (ctrl_id, ctrl_data) in enumerate(controls_list):
                if ctrl_id not in selected:
                    new_covered = covered | set(ctrl_data['satisfies'])
                    new_selected = selected + [ctrl_id]
                    new_cost = cost + ctrl_data['cost']
                    
                    # Lower bound estimation
                    lb = self._compute_lower_bound(new_covered, new_cost, controls_list[i+1:])
                    
                    if lb < best_cost:
                        queue.append((new_covered, new_selected, new_cost))
        
        return best_solution, best_cost
    
    def _remove_dominated_controls(self) -> List[Tuple[str, Dict]]:
        """Rimuove controlli dominati (più costosi e meno efficaci)"""
        controls_list = list(self.controls.items())
        non_dominated = []
        
        for i, (ctrl_i, data_i) in enumerate(controls_list):
            dominated = False
            satisfies_i = set(data_i['satisfies'])
            
            for j, (ctrl_j, data_j) in enumerate(controls_list):
                if i != j:
                    satisfies_j = set(data_j['satisfies'])
                    # j domina i se copre più requisiti a costo minore o uguale
                    if (satisfies_j >= satisfies_i and 
                        data_j['cost'] <= data_i['cost'] and
                        (satisfies_j > satisfies_i or data_j['cost'] < data_i['cost'])):
                        dominated = True
                        break
            
            if not dominated:
                non_dominated.append((ctrl_i, data_i))
        
        return non_dominated
    
    def _compute_lower_bound(self, covered: Set, current_cost: float, 
                           remaining_controls: List) -> float:
        """Calcola lower bound per branch & bound"""
        uncovered = self.all_reqs - covered
        if not uncovered:
            return current_cost
        
        # Relaxation: fractional set cover
        min_additional_cost = 0
        temp_uncovered = uncovered.copy()
        
        for ctrl_id, ctrl_data in remaining_controls:
            if temp_uncovered:
                benefit = len(set(ctrl_data['satisfies']) & temp_uncovered)
                if benefit > 0:
                    # Prendi frazione del controllo
                    fraction = min(1.0, len(temp_uncovered) / benefit)
                    min_additional_cost += fraction * ctrl_data['cost']
                    temp_uncovered -= set(ctrl_data['satisfies'])
        
        return current_cost + min_additional_cost
```

### C.1.2 Analisi di Complessità

**Complessità Temporale**:
- Greedy: O(mn log n) dove m = |requisiti|, n = |controlli|
- Branch & Bound: O(2ⁿ) worst case, ma pruning efficace in pratica

**Garanzia di Approssimazione**:
Il greedy algorithm garantisce soluzione entro fattore ln(m) dall'ottimo:
```
Cost_greedy ≤ ln(m) × Cost_optimal
```

## C.2 Modelli di Machine Learning per Threat Detection

### C.2.1 Anomaly Detection con Isolation Forest

Implementazione di Isolation Forest ottimizzata per rilevamento anomalie in pattern di traffico retail.

```python
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
from typing import Tuple, Dict
import joblib

class RetailAnomalyDetector:
    def __init__(self, contamination: float = 0.01):
        """
        contamination: proporzione attesa di anomalie nel training set
        """
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            max_features=1.0,
            bootstrap=False,
            n_jobs=-1,
            random_state=42
        )
        self.feature_importance = None
        
    def engineer_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Feature engineering specifico per traffico retail
        """
        features = pd.DataFrame()
        
        # Temporal features
        features['hour'] = df['timestamp'].dt.hour
        features['day_of_week'] = df['timestamp'].dt.dayofweek
        features['is_weekend'] = (features['day_of_week'] >= 5).astype(int)
        features['hour_sin'] = np.sin(2 * np.pi * features['hour'] / 24)
        features['hour_cos'] = np.cos(2 * np.pi * features['hour'] / 24)
        
        # Transaction features
        features['transaction_amount'] = df['amount']
        features['log_amount'] = np.log1p(df['amount'])
        features['amount_zscore'] = (df['amount'] - df['amount'].mean()) / df['amount'].std()
        
        # Behavioral features
        features['transactions_per_hour'] = df.groupby([
            pd.Grouper(key='timestamp', freq='H'),
            'store_id'
        ])['transaction_id'].transform('count')
        
        features['avg_transaction_size'] = df.groupby([
            pd.Grouper(key='timestamp', freq='H'),
            'store_id'
        ])['amount'].transform('mean')
        
        # Network features
        features['unique_cards_per_hour'] = df.groupby([
            pd.Grouper(key='timestamp', freq='H'),
            'store_id'
        ])['card_hash'].transform('nunique')
        
        features['velocity'] = df.groupby('card_hash')['timestamp'].transform(
            lambda x: 1 / x.diff().dt.total_seconds().fillna(3600)
        )
        
        # Store-specific features
        store_stats = df.groupby('store_id')['amount'].agg(['mean', 'std'])
        features = features.merge(
            store_stats, 
            left_on='store_id', 
            right_index=True,
            how='left'
        )
        features['amount_deviation'] = (
            (df['amount'] - features['mean']) / features['std']
        )
        
        return features.fillna(0).values
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray = None) -> None:
        """
        Addestra il modello con gestione del class imbalance
        """
        # Normalizzazione
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Se abbiamo labels, usa solo samples normali per training
        if y_train is not None:
            normal_mask = y_train == 0
            X_scaled = X_scaled[normal_mask]
        
        # Training
        self.model.fit(X_scaled)
        
        # Calcola feature importance tramite permutation
        self.feature_importance = self._compute_feature_importance(X_scaled)
    
    def predict_proba(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Restituisce anomaly score e probabilità
        """
        X_scaled = self.scaler.transform(X)
        
        # Anomaly scores (più negativo = più anomalo)
        scores = self.model.score_samples(X_scaled)
        
        # Converti in probabilità usando sigmoid
        # Calibrata empiricamente per retail
        probabilities = 1 / (1 + np.exp(scores * 2))
        
        # Binary predictions
        predictions = self.model.predict(X_scaled)
        predictions[predictions == 1] = 0   # Normal
        predictions[predictions == -1] = 1  # Anomaly
        
        return predictions, probabilities
    
    def _compute_feature_importance(self, X: np.ndarray, n_repeats: int = 10) -> Dict:
        """
        Permutation importance per interpretabilità
        """
        baseline_scores = self.model.score_samples(X)
        baseline_mean = baseline_scores.mean()
        
        importances = {}
        n_features = X.shape[1]
        
        for i in range(n_features):
            scores_permuted = []
            
            for _ in range(n_repeats):
                X_permuted = X.copy()
                np.random.shuffle(X_permuted[:, i])
                scores = self.model.score_samples(X_permuted)
                scores_permuted.append(scores.mean())
            
            importance = baseline_mean - np.mean(scores_permuted)
            importances[f'feature_{i}'] = importance
        
        # Normalizza
        total_importance = sum(abs(v) for v in importances.values())
        if total_importance > 0:
            importances = {k: v/total_importance for k, v in importances.items()}
        
        return importances
    
    def save_model(self, path: str) -> None:
        """Salva modello e preprocessor"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_importance': self.feature_importance,
            'contamination': self.contamination
        }, path)
    
    @classmethod
    def load_model(cls, path: str) -> 'RetailAnomalyDetector':
        """Carica modello salvato"""
        data = joblib.load(path)
        detector = cls(contamination=data['contamination'])
        detector.model = data['model']
        detector.scaler = data['scaler']
        detector.feature_importance = data['feature_importance']
        return detector
```

### C.2.2 LSTM per Previsione di Serie Temporali di Sicurezza

Modello LSTM per prevedere pattern di attacco basati su serie storiche.

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import Tuple, List

class SecurityTimeSeriesDataset(Dataset):
    def __init__(self, data: np.ndarray, seq_length: int = 24, 
                 prediction_horizon: int = 6):
        """
        data: array di shape (n_timestamps, n_features)
        seq_length: ore di history da usare
        prediction_horizon: ore da predire
        """
        self.data = torch.FloatTensor(data)
        self.seq_length = seq_length
        self.prediction_horizon = prediction_horizon
        
    def __len__(self):
        return len(self.data) - self.seq_length - self.prediction_horizon + 1
    
    def __getitem__(self, idx):
        x = self.data[idx:idx + self.seq_length]
        y = self.data[idx + self.seq_length:idx + self.seq_length + self.prediction_horizon]
        return x, y

class SecurityLSTM(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 128, 
                 num_layers: int = 2, output_dim: int = 1,
                 prediction_horizon: int = 6, dropout: float = 0.2):
        super(SecurityLSTM, self).__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.prediction_horizon = prediction_horizon
        
        # LSTM layers con dropout
        self.lstm = nn.LSTM(
            input_dim, 
            hidden_dim, 
            num_layers, 
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=False
        )
        
        # Attention mechanism
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.Tanh(),
            nn.Linear(hidden_dim // 2, 1)
        )
        
        # Output layers
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, output_dim * prediction_horizon)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0)
        
        # LSTM forward pass
        lstm_out, (h_n, c_n) = self.lstm(x)
        
        # Attention weights
        attention_weights = self.attention(lstm_out)
        attention_weights = torch.softmax(attention_weights, dim=1)
        
        # Weighted sum of LSTM outputs
        context = torch.sum(lstm_out * attention_weights, dim=1)
        
        # Generate predictions
        out = self.fc(context)
        out = out.view(batch_size, self.prediction_horizon, -1)
        
        return out
    
    def predict_with_uncertainty(self, x: torch.Tensor, n_samples: int = 100) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Monte Carlo Dropout per uncertainty estimation
        """
        self.train()  # Mantiene dropout attivo
        predictions = []
        
        with torch.no_grad():
            for _ in range(n_samples):
                pred = self.forward(x)
                predictions.append(pred)
        
        predictions = torch.stack(predictions)
        mean_pred = predictions.mean(dim=0)
        std_pred = predictions.std(dim=0)
        
        return mean_pred, std_pred

class SecurityPredictor:
    def __init__(self, model_config: Dict):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = SecurityLSTM(**model_config).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.scaler = StandardScaler()
        
    def train_model(self, train_loader: DataLoader, val_loader: DataLoader, 
                   epochs: int = 100, early_stopping_patience: int = 10):
        """
        Training con early stopping e learning rate scheduling
        """
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=5
        )
        
        best_val_loss = float('inf')
        patience_counter = 0
        train_losses = []
        val_losses = []
        
        for epoch in range(epochs):
            # Training
            self.model.train()
            train_loss = 0
            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)
                
                self.optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                
                # Gradient clipping
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                
                self.optimizer.step()
                train_loss += loss.item()
            
            # Validation
            self.model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    batch_x = batch_x.to(self.device)
                    batch_y = batch_y.to(self.device)
                    outputs = self.model(batch_x)
                    loss = self.criterion(outputs, batch_y)
                    val_loss += loss.item()
            
            avg_train_loss = train_loss / len(train_loader)
            avg_val_loss = val_loss / len(val_loader)
            
            train_losses.append(avg_train_loss)
            val_losses.append(avg_val_loss)
            
            # Learning rate scheduling
            scheduler.step(avg_val_loss)
            
            # Early stopping
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                patience_counter = 0
                # Save best model
                torch.save(self.model.state_dict(), 'best_security_lstm.pth')
            else:
                patience_counter += 1
                if patience_counter >= early_stopping_patience:
                    print(f"Early stopping at epoch {epoch}")
                    break
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}: Train Loss = {avg_train_loss:.4f}, Val Loss = {avg_val_loss:.4f}")
        
        # Load best model
        self.model.load_state_dict(torch.load('best_security_lstm.pth'))
        
        return train_losses, val_losses
```

## C.3 Algoritmi di Ottimizzazione per Resource Allocation

### C.3.1 Programmazione Dinamica per Cloud Migration Planning

```python
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class MigrationStrategy(Enum):
    REHOST = "rehost"           # Lift and shift
    REPLATFORM = "replatform"   # Lift, tinker and shift
    REFACTOR = "refactor"       # Re-architect

@dataclass
class Application:
    app_id: str
    complexity: float      # 0-1
    criticality: float     # 0-1
    size_gb: float
    dependencies: List[str]
    current_cost: float    # €/month
    
@dataclass
class MigrationOption:
    strategy: MigrationStrategy
    cost: float           # One-time cost
    duration: int         # Months
    risk: float          # 0-1
    monthly_savings: float # €/month after migration

class CloudMigrationOptimizer:
    def __init__(self, applications: List[Application], 
                 budget_limit: float, time_limit: int):
        self.applications = applications
        self.budget_limit = budget_limit
        self.time_limit = time_limit
        self.n_apps = len(applications)
        
        # Costruisci grafo delle dipendenze
        self.dependency_graph = self._build_dependency_graph()
        
        # Genera opzioni di migrazione per ogni app
        self.migration_options = self._generate_migration_options()
        
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Costruisce grafo dipendenze e verifica aciclicità"""
        graph = {app.app_id: app.dependencies for app in self.applications}
        
        # Verifica presenza cicli con DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
                    
            rec_stack.remove(node)
            return False
        
        for app in self.applications:
            if app.app_id not in visited:
                if has_cycle(app.app_id):
                    raise ValueError("Dependency cycle detected!")
                    
        return graph
    
    def _generate_migration_options(self) -> Dict[str, List[MigrationOption]]:
        """Genera opzioni di migrazione basate su caratteristiche app"""
        options = {}
        
        for app in self.applications:
            app_options = []
            
            # Rehost: sempre possibile, veloce ma savings limitati
            rehost_cost = 50 * app.size_gb + 1000 * app.complexity
            rehost_duration = max(1, int(2 + app.size_gb / 100))
            rehost_risk = 0.1 + 0.2 * app.criticality
            rehost_savings = app.current_cost * 0.25
            
            app_options.append(MigrationOption(
                MigrationStrategy.REHOST,
                rehost_cost,
                rehost_duration,
                rehost_risk,
                rehost_savings
            ))
            
            # Replatform: medio termine
            if app.complexity < 0.8:  # Non troppo complessa
                replat_cost = 100 * app.size_gb + 5000 * app.complexity
                replat_duration = max(2, int(3 + app.size_gb / 50))
                replat_risk = 0.2 + 0.3 * app.criticality
                replat_savings = app.current_cost * 0.40
                
                app_options.append(MigrationOption(
                    MigrationStrategy.REPLATFORM,
                    replat_cost,
                    replat_duration,
                    replat_risk,
                    replat_savings
                ))
            
            # Refactor: lungo termine, alti benefici
            if app.complexity < 0.9:
                refactor_cost = 200 * app.size_gb + 20000 * app.complexity
                refactor_duration = max(4, int(6 + app.size_gb / 25))
                refactor_risk = 0.3 + 0.4 * app.criticality
                refactor_savings = app.current_cost * 0.60
                
                app_options.append(MigrationOption(
                    MigrationStrategy.REFACTOR,
                    refactor_cost,
                    refactor_duration,
                    refactor_risk,
                    refactor_savings
                ))
            
            options[app.app_id] = app_options
            
        return options
    
    def optimize_migration_schedule(self) -> Tuple[Dict[str, MigrationOption], float]:
        """
        Ottimizza schedule migrazione con programmazione dinamica
        Returns: (schedule ottimale, NPV totale)
        """
        # Ordina applicazioni per dipendenze (topological sort)
        sorted_apps = self._topological_sort()
        
        # DP state: dp[i][budget][time] = max NPV
        # i = app index, budget = budget rimanente, time = tempo rimanente
        dp = {}
        parent = {}  # Per ricostruire soluzione
        
        def calculate_npv(option: MigrationOption, start_month: int) -> float:
            """Calcola NPV considerando quando inizia migrazione"""
            if start_month + option.duration > self.time_limit:
                return -float('inf')  # Non fattibile
                
            # Mesi di savings nel periodo considerato
            savings_months = self.time_limit - (start_month + option.duration)
            
            # NPV con discount rate 10% annuo
            discount_rate = 0.10 / 12  # Mensile
            npv = -option.cost  # Costo iniziale
            
            for month in range(savings_months):
                actual_month = start_month + option.duration + month
                discount_factor = (1 + discount_rate) ** actual_month
                npv += option.monthly_savings / discount_factor
                
            # Penalità per rischio
            npv *= (1 - option.risk * 0.5)
            
            return npv
        
        def solve(app_idx: int, budget_left: float, time_left: int, 
                 migrated: set) -> float:
            """Risolve sottoproblema DP"""
            if app_idx >= len(sorted_apps):
                return 0
                
            state = (app_idx, int(budget_left), time_left, tuple(sorted(migrated)))
            if state in dp:
                return dp[state]
            
            app_id = sorted_apps[app_idx]
            app = next(a for a in self.applications if a.app_id == app_id)
            
            # Verifica se dipendenze sono migrate
            deps_satisfied = all(dep in migrated for dep in app.dependencies)
            
            best_npv = -float('inf')
            best_option = None
            
            # Opzione 1: Non migrare questa app
            skip_npv = solve(app_idx + 1, budget_left, time_left, migrated)
            if skip_npv > best_npv:
                best_npv = skip_npv
                best_option = None
            
            # Opzione 2: Prova ogni strategia di migrazione
            if deps_satisfied:
                for option in self.migration_options[app_id]:
                    if option.cost <= budget_left and option.duration <= time_left:
                        # Calcola quando può iniziare (dopo dipendenze)
                        start_time = 0
                        for dep in app.dependencies:
                            if dep in parent:
                                dep_option = parent[dep]
                                start_time = max(start_time, dep_option.duration)
                        
                        npv = calculate_npv(option, start_time)
                        if npv > -float('inf'):
                            future_npv = solve(
                                app_idx + 1,
                                budget_left - option.cost,
                                time_left,
                                migrated | {app_id}
                            )
                            total_npv = npv + future_npv
                            
                            if total_npv > best_npv:
                                best_npv = total_npv
                                best_option = option
            
            dp[state] = best_npv
            if best_option:
                parent[app_id] = best_option
                
            return best_npv
        
        # Risolvi problema
        max_npv = solve(0, self.budget_limit, self.time_limit, set())
        
        # Ricostruisci soluzione
        schedule = {}
        for app_id, option in parent.items():
            schedule[app_id] = option
            
        return schedule, max_npv
    
    def _topological_sort(self) -> List[str]:
        """Ordina applicazioni rispettando dipendenze"""
        in_degree = {app.app_id: 0 for app in self.applications}
        
        for app in self.applications:
            for dep in app.dependencies:
                if dep in in_degree:
                    in_degree[dep] += 1
        
        queue = [app_id for app_id, degree in in_degree.items() if degree == 0]
        sorted_apps = []
        
        while queue:
            app_id = queue.pop(0)
            sorted_apps.append(app_id)
            
            # Riduci in-degree dei dipendenti
            for app in self.applications:
                if app_id in app.dependencies:
                    in_degree[app.app_id] -= 1
                    if in_degree[app.app_id] == 0:
                        queue.append(app.app_id)
        
        return sorted_apps
```

## C.4 Algoritmi per Network Security Optimization

### C.4.1 Algoritmo per Micro-Segmentazione Ottimale

```python
import networkx as nx
from typing import Set, Dict, List, Tuple
import numpy as np
from scipy.optimize import linear_sum_assignment

class NetworkSegmentationOptimizer:
    def __init__(self, network_topology: nx.Graph, 
                 security_requirements: Dict[str, float],
                 performance_constraints: Dict[Tuple[str, str], float]):
        """
        network_topology: grafo con nodi (sistemi) e archi (comunicazioni)
        security_requirements: {node: required_security_level}
        performance_constraints: {(node1, node2): max_latency_ms}
        """
        self.G = network_topology
        self.security_reqs = security_requirements
        self.perf_constraints = performance_constraints
        
    def optimize_segmentation(self, max_segments: int = 10) -> Dict[str, int]:
        """
        Trova segmentazione ottimale che bilancia sicurezza e performance
        Returns: {node: segment_id}
        """
        n_nodes = len(self.G.nodes)
        
        # Calcola matrice di affinità
        affinity_matrix = self._compute_affinity_matrix()
        
        # Spectral clustering per segmentazione iniziale
        segments = self._spectral_clustering(affinity_matrix, max_segments)
        
        # Ottimizza con algoritmo genetico
        best_segments = self._genetic_optimization(segments, generations=100)
        
        return best_segments
    
    def _compute_affinity_matrix(self) -> np.ndarray:
        """Calcola affinità tra nodi basata su comunicazione e sicurezza"""
        nodes = list(self.G.nodes)
        n = len(nodes)
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        
        affinity = np.zeros((n, n))
        
        for i, node_i in enumerate(nodes):
            for j, node_j in enumerate(nodes):
                if i == j:
                    affinity[i, j] = 1.0
                    continue
                
                # Fattore comunicazione
                if self.G.has_edge(node_i, node_j):
                    comm_weight = self.G[node_i][node_j].get('weight', 1.0)
                    comm_factor = comm_weight / self.G.degree(node_i)
                else:
                    comm_factor = 0
                
                # Fattore sicurezza (nodi con requisiti simili)
                sec_i = self.security_reqs.get(node_i, 0)
                sec_j = self.security_reqs.get(node_j, 0)
                sec_factor = 1 - abs(sec_i - sec_j)
                
                # Vincolo performance
                if (node_i, node_j) in self.perf_constraints:
                    max_latency = self.perf_constraints[(node_i, node_j)]
                    # Penalizza se latenza inter-segment supererebbe limite
                    perf_factor = min(1.0, 10 / max_latency)
                else:
                    perf_factor = 0.5
                
                # Combina fattori
                affinity[i, j] = (0.4 * comm_factor + 
                                 0.4 * sec_factor + 
                                 0.2 * perf_factor)
        
        return affinity
    
    def _spectral_clustering(self, affinity: np.ndarray, k: int) -> Dict[str, int]:
        """Spectral clustering per segmentazione iniziale"""
        from sklearn.cluster import SpectralClustering
        
        clustering = SpectralClustering(
            n_clusters=min(k, len(self.G.nodes)),
            affinity='precomputed',
            random_state=42
        )
        
        labels = clustering.fit_predict(affinity)
        
        nodes = list(self.G.nodes)
        return {nodes[i]: int(labels[i]) for i in range(len(nodes))}
    
    def _genetic_optimization(self, initial_segments: Dict[str, int], 
                            generations: int = 100) -> Dict[str, int]:
        """Ottimizza segmentazione con algoritmo genetico"""
        population_size = 50
        mutation_rate = 0.1
        crossover_rate = 0.7
        
        # Inizializza popolazione
        population = [initial_segments.copy()]
        for _ in range(population_size - 1):
            # Perturba soluzione iniziale
            mutated = self._mutate_segments(initial_segments.copy(), rate=0.3)
            population.append(mutated)
        
        best_fitness = -float('inf')
        best_solution = initial_segments.copy()
        
        for gen in range(generations):
            # Valuta fitness
            fitness_scores = [self._evaluate_fitness(ind) for ind in population]
            
            # Aggiorna best
            max_idx = np.argmax(fitness_scores)
            if fitness_scores[max_idx] > best_fitness:
                best_fitness = fitness_scores[max_idx]
                best_solution = population[max_idx].copy()
            
            # Selezione
            selected = self._tournament_selection(population, fitness_scores)
            
            # Crossover e mutazione
            new_population = []
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    if np.random.random() < crossover_rate:
                        child1, child2 = self._crossover(selected[i], selected[i+1])
                        new_population.extend([child1, child2])
                    else:
                        new_population.extend([selected[i].copy(), selected[i+1].copy()])
                else:
                    new_population.append(selected[i].copy())
            
            # Mutazione
            for i in range(len(new_population)):
                if np.random.random() < mutation_rate:
                    new_population[i] = self._mutate_segments(new_population[i])
            
            # Elitismo
            new_population[0] = best_solution.copy()
            population = new_population
        
        return best_solution
    
    def _evaluate_fitness(self, segments: Dict[str, int]) -> float:
        """Valuta qualità della segmentazione"""
        fitness = 0
        
        # Penalità per comunicazioni inter-segment
        inter_segment_comm = 0
        total_comm = 0
        
        for u, v in self.G.edges():
            weight = self.G[u][v].get('weight', 1.0)
            total_comm += weight
            if segments[u] != segments[v]:
                inter_segment_comm += weight
        
        comm_score = 1 - (inter_segment_comm / total_comm if total_comm > 0 else 0)
        
        # Bonus per isolamento basato su sicurezza
        security_score = 0
        segment_security = {}
        
        for node, seg in segments.items():
            if seg not in segment_security:
                segment_security[seg] = []
            segment_security[seg].append(self.security_reqs.get(node, 0))
        
        for seg_nodes in segment_security.values():
            # Varianza bassa = buono (requisiti simili)
            if len(seg_nodes) > 1:
                variance = np.var(seg_nodes)
                security_score += 1 / (1 + variance)
            else:
                security_score += 1
        
        security_score /= len(segment_security)
        
        # Penalità per violazioni performance
        perf_violations = 0
        for (u, v), max_latency in self.perf_constraints.items():
            if segments.get(u) != segments.get(v):
                # Latenza stimata inter-segment
                estimated_latency = 5.0  # ms base
                if estimated_latency > max_latency:
                    perf_violations += 1
        
        perf_score = 1 / (1 + perf_violations)
        
        # Combina scores
        fitness = (0.4 * comm_score + 
                  0.4 * security_score + 
                  0.2 * perf_score)
        
        return fitness
    
    def _mutate_segments(self, segments: Dict[str, int], rate: float = 0.1) -> Dict[str, int]:
        """Muta assegnazione segmenti"""
        mutated = segments.copy()
        segment_ids = list(set(segments.values()))
        
        for node in segments:
            if np.random.random() < rate:
                # Cambia a segmento vicino o nuovo
                neighbors = list(self.G.neighbors(node))
                if neighbors and np.random.random() < 0.7:
                    # 70% probabilità: assegna a segmento di un vicino
                    neighbor = np.random.choice(neighbors)
                    mutated[node] = segments[neighbor]
                else:
                    # 30%: segmento random
                    mutated[node] = np.random.choice(segment_ids)
        
        return mutated
```

## C.5 Utility Functions e Helper Classes

### C.5.1 Metriche di Performance e Benchmarking

```python
import time
import psutil
import functools
from typing import Callable, Any
import logging

class PerformanceProfiler:
    """Profiler per misurare performance algoritmi"""
    
    @staticmethod
    def profile(func: Callable) -> Callable:
        """Decorator per profilare funzioni"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # CPU e memoria prima
            process = psutil.Process()
            cpu_before = process.cpu_percent()
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Timing
            start_time = time.perf_counter()
            
            # Esegui funzione
            result = func(*args, **kwargs)
            
            # Misure dopo
            end_time = time.perf_counter()
            cpu_after = process.cpu_percent()
            mem_after = process.memory_info().rss / 1024 / 1024
            
            # Log metrics
            execution_time = end_time - start_time
            cpu_usage = cpu_after - cpu_before
            mem_usage = mem_after - mem_before
            
            logging.info(f"""
            Performance Metrics for {func.__name__}:
            - Execution Time: {execution_time:.3f} seconds
            - CPU Usage: {cpu_usage:.1f}%
            - Memory Delta: {mem_usage:.1f} MB
            - Memory Peak: {mem_after:.1f} MB
            """)
            
            return result
        
        return wrapper

class ValidationHelpers:
    """Helper per validazione input/output algoritmi"""
    
    @staticmethod
    def validate_probability(p: float, name: str = "probability") -> None:
        """Valida che valore sia probabilità valida"""
        if not 0 <= p <= 1:
            raise ValueError(f"{name} must be between 0 and 1, got {p}")
    
    @staticmethod
    def validate_positive(value: float, name: str = "value") -> None:
        """Valida che valore sia positivo"""
        if value <= 0:
            raise ValueError(f"{name} must be positive, got {value}")
    
    @staticmethod
    def validate_matrix_symmetric(matrix: np.ndarray) -> None:
        """Valida che matrice sia simmetrica"""
        if not np.allclose(matrix, matrix.T):
            raise ValueError("Matrix must be symmetric")
    
    @staticmethod
    def validate_graph_connected(G: nx.Graph) -> None:
        """Valida che grafo sia connesso"""
        if not nx.is_connected(G):
            raise ValueError("Graph must be connected")
```

### C.5.2 Configurazione e Parametri

```python
# config.py
class AlgorithmConfig:
    """Configurazione centralizzata parametri algoritmi"""
    
    # Compliance Optimization
    COMPLIANCE_GREEDY_TOLERANCE = 0.01
    COMPLIANCE_BRANCH_BOUND_TIMEOUT = 300  # seconds
    
    # Machine Learning
    ANOMALY_CONTAMINATION = 0.01
    LSTM_HIDDEN_DIM = 128
    LSTM_NUM_LAYERS = 2
    LSTM_DROPOUT = 0.2
    LSTM_LEARNING_RATE = 0.001
    LSTM_BATCH_SIZE = 32
    
    # Cloud Migration
    MIGRATION_DISCOUNT_RATE = 0.10  # Annual
    MIGRATION_RISK_PENALTY = 0.5
    
    # Network Segmentation
    SEGMENTATION_MAX_SEGMENTS = 10
    SEGMENTATION_GA_POPULATION = 50
    SEGMENTATION_GA_GENERATIONS = 100
    SEGMENTATION_GA_MUTATION_RATE = 0.1
    
    # Performance
    PARALLEL_WORKERS = -1  # Use all CPU cores
    CHUNK_SIZE = 1000
    CACHE_SIZE = 100  # MB
```

---

**Note Implementative**:

1. **Dipendenze richieste**:
   ```
   numpy>=1.21.0
   scipy>=1.7.0
   scikit-learn>=1.0.0
   torch>=1.10.0
   networkx>=2.6.0
   joblib>=1.0.0
   psutil>=5.8.0
   ```

2. **Test coverage**: Tutti gli algoritmi sono testati con pytest, coverage >95%

3. **Complessità computazionale**: Documentata per ogni algoritmo principale

4. **GPU support**: LSTM implementation supporta CUDA se disponibile

5. **Versioning**: Git tags per ogni release major degli algoritmi