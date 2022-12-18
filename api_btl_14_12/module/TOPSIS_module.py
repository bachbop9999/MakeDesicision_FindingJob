import numpy as np
import warnings

class Topsis():
    evaluation_matrix = np.array([])  # Matrix
    weighted_normalized = np.array([])  # Weight matrix
    normalized_decision = np.array([])  # Normalisation matrix
    M = 0  # Number of rows
    N = 0  # Number of columns

    '''
    # Step 1
	Create an evaluation matrix consisting of m alternatives and n criteria,
	with the intersection of each alternative and criteria given as {\displaystyle x_{ij}}x_{ij},
	we therefore have a matrix {\displaystyle (x_{ij})_{m\times n}}(x_{{ij}})_{{m\times n}}.
	'''
    def __init__(self, evaluation_matrix, weight_matrix, criteria):
        # M×N matrix
        self.evaluation_matrix = np.array(evaluation_matrix, dtype="float")

        # M alternatives (options)
        self.row_size = len(self.evaluation_matrix)

        # N attributes/criteria
        self.column_size = len(self.evaluation_matrix[0])

        # N size weight matrix
        self.weight_matrix = np.array(weight_matrix, dtype="float")
        self.weight_matrix = self.weight_matrix/sum(self.weight_matrix)
        self.criteria = np.array(criteria, dtype="float")
    
    '''
	# Step 2
	The matrix {\displaystyle (x_{ij})_{m\times n}}(x_{{ij}})_{{m\times n}} is then normalised to form the matrix
	'''
    def step_2(self):
        # normalized scores
        self.normalized_decision = np.copy(self.evaluation_matrix)
        sqrd_sum = np.zeros(self.column_size)
        for i in range(self.row_size):
            for j in range(self.column_size):
                sqrd_sum[j] += self.evaluation_matrix[i, j]**2
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.normalized_decision[i, j] = self.evaluation_matrix[i, j]/(sqrd_sum[j]**0.5)

    '''
	# Step 3
	Calculate the weighted normalised decision matrix
	'''
    def step_3(self):
        from pdb import set_trace
        self.weighted_normalized = np.copy(self.normalized_decision)
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.weighted_normalized[i, j] *= self.weight_matrix[j]

    '''
	# Step 4
	Determine the worst alternative {\displaystyle (A_{w})}(A_{w}) and the best alternative {\displaystyle (A_{b})}(A_{b}):
	'''
    def step_4(self):
        self.worst_alternatives = np.zeros(self.column_size)
        self.best_alternatives = np.zeros(self.column_size)
        for i in range(self.column_size):
            if self.criteria[i]:
                self.worst_alternatives[i] = min(
                    self.weighted_normalized[:, i])
                self.best_alternatives[i] = max(self.weighted_normalized[:, i])
            else:
                self.worst_alternatives[i] = max(
                    self.weighted_normalized[:, i])
                self.best_alternatives[i] = min(self.weighted_normalized[:, i])

    '''
	# Step 5
	Calculate the L2-distance between the target alternative {\displaystyle i}i and the worst condition {\displaystyle A_{w}}A_{w}
	{\displaystyle d_{iw}={\sqrt {\sum _{j=1}^{n}(t_{ij}-t_{wj})^{2}}},\quad i=1,2,\ldots ,m,}
	and the distance between the alternative {\displaystyle i}i and the best condition {\displaystyle A_{b}}A_b
	{\displaystyle d_{ib}={\sqrt {\sum _{j=1}^{n}(t_{ij}-t_{bj})^{2}}},\quad i=1,2,\ldots ,m}
	where {\displaystyle d_{iw}}d_{{iw}} and {\displaystyle d_{ib}}d_{{ib}} are L2-norm distances 
	from the target alternative {\displaystyle i}i to the worst and best conditions, respectively.
	'''
    def step_5(self):
        self.worst_distance = np.zeros(self.row_size)
        self.best_distance = np.zeros(self.row_size)

        self.worst_distance_mat = np.copy(self.weighted_normalized)
        self.best_distance_mat = np.copy(self.weighted_normalized)

        for i in range(self.row_size):
            for j in range(self.column_size):
                self.worst_distance_mat[i][j] = (self.weighted_normalized[i][j]-self.worst_alternatives[j])**2
                self.best_distance_mat[i][j] = (self.weighted_normalized[i][j]-self.best_alternatives[j])**2
                
                self.worst_distance[i] += self.worst_distance_mat[i][j]
                self.best_distance[i] += self.best_distance_mat[i][j]

        for i in range(self.row_size):
            self.worst_distance[i] = self.worst_distance[i]**0.5
            self.best_distance[i] = self.best_distance[i]**0.5

    '''
	# Step 6
	Calculate the similarity
	'''
    def step_6(self):
        np.seterr(all='ignore')
        self.worst_similarity = np.zeros(self.row_size)
        self.best_similarity = np.zeros(self.row_size)

        for i in range(self.row_size):
            # calculate the similarity to the worst condition
            self.worst_similarity[i] = self.worst_distance[i] / \
                (self.worst_distance[i]+self.best_distance[i])

            # calculate the similarity to the best condition
            self.best_similarity[i] = self.best_distance[i] / \
                (self.worst_distance[i]+self.best_distance[i])
    
    def ranking(self, data):
        return [i+1 for i in data.argsort()]

    def rank_to_worst_similarity(self):
        # return rankdata(self.worst_similarity, method="min").astype(int)
        return self.ranking(self.worst_similarity)

    def rank_to_best_similarity(self):
        # return rankdata(self.best_similarity, method='min').astype(int)
        return self.ranking(self.best_similarity)

    def calc(self):
        print("Step 1: Create an evaluation matrix consisting\n", self.evaluation_matrix, end="\n\n")
        
        self.step_2()
        print("Step 2: The  normalised matrix\n", self.normalized_decision, end="\n\n")
        
        self.step_3()
        print("Step 3: Calculate the weighted normalised decision matrix\n", self.weighted_normalized, end="\n\n")
        
        self.step_4()
        print("Step 4: Determine the worst alternative and the best alternative\n", self.worst_alternatives,
              self.best_alternatives, end="\n\n")
        
        self.step_5()
        print("Step 5: Calculate the L2-distance\n", self.worst_distance, self.best_distance, end="\n\n")
        
        self.step_6()
        print("Step 6: Calculate the similarity\n", self.worst_similarity,
              self.best_similarity, end="\n\n")

def normalize_employee_salary_min(er_salary,ee_salary):
    deviation = ee_salary - er_salary
    if deviation == 0:
        return 20
    elif deviation > 0:
        return (er_salary / abs(deviation))*0.4
    else:
        return (er_salary / abs(deviation))*0.6
def normalize_employee_salary_max(er_salary,ee_salary):
    deviation = ee_salary - er_salary
    if deviation == 0:
        return 20
    elif deviation > 0:
        return (er_salary / abs(deviation))*0.6
    else:
        return (er_salary / abs(deviation))*0.4
max_degree = 5
def normalize_degree(er_degree,ee_degree):
    deviation = ee_degree - er_degree
    if deviation == 0:
        return 3
    elif deviation > 0:
        return (max_degree / abs(deviation))*0.6
    else:
        return (max_degree / abs(deviation))*0.4
def normalize_experience(er_experience,ee_experience):
    deviation = ee_experience - er_experience
    if deviation == 0:
        return 5
    elif deviation > 0:
        return (er_experience / abs(deviation))*0.6
    else:
        return (er_experience / abs(deviation))*0.4
def normalize_location(ee,er):
#     [(5000000.0, 10000000.0, 5, 2.0, 2, 1, 10),
    if ee[6] == er[6]:
        return 9
    elif ee[5] == er[5]:
        return 5
    else:
        return 3
def get_mark_career(c1,c2):
#     map_key = {'C# Backend Developer':0, 'Java Backend Developer':1, 'Python Developer':2, 'React Frontend Developer':3, 'Data engineer':4}
#     dict_value = {'C# Backend Developer' : [1.0, 0.1, 0.3, 0.2, 0.25],
#                     'Java Backend Developer' : [0.1, 1.0, 0.2, 0.3, 0.15],
#                     'Python Developer' : [0.3, 0.2, 1.0, 0.4, 0.35],
#                     'React Frontend Developer' : [0.2, 0.3, 0.4, 1.0, 0.25],
#                     'Data engineer' : [0.25, 0.15, 0.35, 0.25, 1.0] }
#     return dict_value[c1][map_key[c2]]

    dict_value = [[1.0, 0.8, 0.5, 0.1, 0.3],
                  [0.8, 1.0, 0.7, 0.1, 0.3],
                  [0.5, 0.7, 1.0, 0.1, 0.6],
                  [0.1, 0.1, 0.1, 1.0, 0.05],
                  [0.3, 0.3, 0.6, 0.05, 1.0]]
    return dict_value[c1-1][c2-1]
#luong_min,luong_max,nghanh_nghe,nam_kinh_nghiem, bang_cap,vi_tri
def normalize_employee(list_jobs,per):
    list_result = []
    for job in list_jobs:
        list_result.append([normalize_employee_salary_min(job[0],per[0]),
            normalize_employee_salary_max(job[1],per[1]),
            get_mark_career(job[2],per[2]),
            normalize_experience(job[3],per[3]),
            normalize_degree(job[4],per[4]),
            normalize_location(job,per)])
    return list_result