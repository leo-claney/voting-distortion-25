from numpy import random
import numpy as np
import scipy as sp
import math
from vote import Vote
from election import Election
import matplotlib.pyplot as plt 


class SVoter3D:
    def __init__(self, num, x, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
        self.id = num
        self.scores = {}

    def setScores(self,scoreDict):
        self.scores = scoreDict

    def __str__(self):
        return "Voter "+str(self.id)

class SCandidate3D:
    def __init__(self, num, x, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.id = num

    def __str__(self):
        return "Candidate "+str(self.id)
    
class VoteResult3D:
    def __init__(self, n, m, dimension = "1D", distribution="normal",strat_voter_percentage=0,strat_vote_type="burial"):
        self.voters = []      #size of voters is n
        self.candidates = []  #size of candidates is m
        self.distribution = distribution
        self.dimension = dimension
        self.SV_percentage = strat_voter_percentage

        #generate random coordinates of voters and candidates for different distributions
        if self.distribution == "normal":
            x_voters = random.normal(50, 18,n)
            x_candidates = random.normal(50, 18, m)
            y_voters = random.normal(50, 18,n)
            y_candidates = random.normal(50, 18, m)
            z_voters = random.normal(50, 18,n)
            z_candidates = random.normal(50, 18, m)
            
            
        elif self.distribution == "poisson":
            x_voters = random.poisson(30, n)
            x_candidates = random.poisson(30, m)
            y_voters = random.poisson(30, n)
            y_candidates = random.poisson(30, m)
            z_voters = random.poisson(30, n)
            z_candidates = random.poisson(30, m)
           

        elif self.distribution == "uniform":
            x_voters = random.uniform(0, 100, n)
            x_candidates = random.uniform(0, 100, m)
            y_voters = random.uniform(0, 100, n)
            y_candidates = random.uniform(0, 100, m)
            z_voters = random.uniform(0, 100, n)
            z_candidates = random.uniform(0, 100, m)
            

        elif self.distribution == "bimodal":
            x_voters1 = random.normal(30, 10, n//2)
            x_voters2 = random.normal(70, 10, n-n//2)
            y_voters1 = random.normal(30,10,n//2)
            y_voters2 = random.normal(70, 10, n-n//2)
            z_voters1 = random.normal(30,10,n//2)
            z_voters2 = random.normal(70, 10, n-n//2)

            x_candidates1 = random.normal(30, 10, m//2)   
            x_candidates2 = random.normal(70, 10, m-m//2)
            y_candidates1 = random.normal(30, 10, m//2)
            y_candidates2 = random.normal(70, 10, m-m//2)
            z_candidates1 = random.normal(30, 10, m//2)
            z_candidates2 = random.normal(70, 10, m-m//2)

            x_voters = np.concatenate((x_voters1, x_voters2), axis=None)
            y_voters = np.concatenate((y_voters1, y_voters2), axis=None)
            z_voters = np.concatenate((z_voters1, z_voters2), axis=None)

            x_candidates = np.concatenate((x_candidates1, x_candidates2), axis = None)
            y_candidates = np.concatenate((y_candidates1, y_candidates2), axis = None)
            z_candidates = np.concatenate((z_candidates1, z_candidates2), axis = None)

        #generate voters and candidates based on the coordinates
        for i in range(n):
            voter = None
            if self.dimension == "1D":
                voter = SVoter3D(i, x_voters[i])
            elif self.dimension == "2D":
                voter = SVoter3D(i, x_voters[i], y_voters[i])
            elif self.dimension == "3D":
                voter = SVoter3D(i, x_voters[i], y_voters[i], z_voters[i])
            
            self.voters.append(voter)

        for i in range(m):
            candidate = None
            if self.dimension == "1D":
                candidate = SCandidate3D(i, x_candidates[i])
            elif self.dimension == "2D":
                candidate = SCandidate3D(i, x_candidates[i], y_candidates[i])
            elif self.dimension == "3D":
                candidate = SCandidate3D(i, x_candidates[i], y_candidates[i], z_candidates[i])
            
            self.candidates.append(candidate)


        self.minDistance = float('inf')
        self.OPTcandidate = self.candidates[0]
        for candidate in self.candidates:
            sumDistance = 0
            for voter in self.voters:
                distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2 + (voter.z - candidate.z) ** 2)
                sumDistance += distance
            if sumDistance < self.minDistance:
                self.minDistance = sumDistance
                self.OPTcandidate = candidate
       
        #get preference profile of each voter given a set of candidates
        #Get the number of strategic voters
        num_of_strat_voters = int(n * strat_voter_percentage)
        count = 0
        self.ballots = []
        for voter in self.voters:
            if count < num_of_strat_voters:
                if strat_vote_type == "burial":
                    #currently sorts as usual, simply need to add the putting of the optimal/second to optimal last
                    distances = {}
                    for candidate in self.candidates:
                        distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2 + (voter.z - candidate.z) ** 2)
                        distances[candidate] = distance         
                    sorted_dict = sorted(distances, key = distances.get)
                    self.ballots.append(sorted_dict)
                #if strat_vote_type == "compromise":
                
                count += 1
            else:
                distances = {}
                for candidate in self.candidates:
                    distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2 + (voter.z - candidate.z) ** 2)
                    distances[candidate] = distance         
                sorted_dict = sorted(distances, key = distances.get)
                self.ballots.append(sorted_dict)
            

    def plurality(self):
        votes = {}
        for ballot in self.ballots:
            if ballot[0] in votes:
                votes[ballot[0]] += 1
            else:
                votes[ballot[0]] = 1
        self.sorted_dict = sorted(votes.items(), key = lambda kv: kv[1], reverse = True)      
        return self.sorted_dict[0][0]

    def borda(self):
        points = {}
        for ballot in self.ballots:
            n = len(ballot)
            i = 1
            for candidate in ballot:
                if candidate in points:
                    points[candidate] += (n - i)
                else:
                    points[candidate] = (n - i)
                i += 1
        sorted_dict = sorted(points.items(), key = lambda kv: kv[1], reverse = True)     
        return sorted_dict[0][0]

    def STV(self):
        votes = []
        for ballot in self.ballots:
            vote = Vote(ballot)
            votes.append(vote)
        election = Election(votes)
        election.run_election()
        winner = election.winner
        
        return winner
    
    def head_to_head(self,c_type=0.5):
        points = {}
        score1 = 0
        score2 = 0
        for i in range(len(self.candidates)):
            for j in range(i + 1, len(self.candidates)):
                for ballot in self.ballots:
                    found = False
                    k = 0
                    while not found:
                        if ballot[k] == self.candidates[i]:
                            score1 += 1
                            found = True
                        elif ballot[k] == self.candidates[j]:
                            score2 += 1
                            found = True
                        k += 1            
                if score1 == score2:
                    if self.candidates[i] in points:
                        points[self.candidates[i]] += c_type
                    else:
                        points[self.candidates[i]] = c_type
                    if self.candidates[j] in points:
                        points[self.candidates[j]] += c_type
                    else:
                        points[self.candidates[j]] = c_type
                elif score1 > score2:
                    if self.candidates[i] in points:
                        points[self.candidates[i]] += 1
                    else:
                        points[self.candidates[i]] = 1
                else:
                    if self.candidates[j] in points:
                        points[self.candidates[j]] += 1
                    else:
                        points[self.candidates[j]] = 1
                score1 = 0
                score2 = 0
        sorted_dict = sorted(points.items(), key = lambda kv: kv[1], reverse = True)
        
        #check if a Condorcet Winner exists
        self.hasCondorcetWinner = False
        if sorted_dict[0][1] == len(self.candidates) - 1:
            self.hasCondorcetWinner = True
            self.condorcetWinner = sorted_dict[0][0]
        return sorted_dict
        
    def copeland(self,c_type=0.5):
        sorted_dict = self.head_to_head(c_type)
        return sorted_dict[0][0]



    def pluralityVeto(self):
        # plurality stage - each candidate is given score equals the number of times they are first-choice
        points = {}
        for ballot in self.ballots:
            if ballot[0] in points:
                points[ballot[0]] += 1
            else:
                points[ballot[0]] = 1
        
        # veto stage 
        numToRemove = len(points) - 1
        while numToRemove>0:
            for ballot in self.ballots:
                # find the bottom-choice candidate among the the standing one
                k = -1
                while not ballot[k] in points:
                    k -= 1

                # decrement score 
                points[ballot[k]] -= 1

                # eleminate the candidate when score reaches 0
                if points[ballot[k]] == 0:
                    points.pop(ballot[k]) 
                    numToRemove -= 1
                    if numToRemove == 0:
                        break
        
        # the last standing candidate is the winner
        winner = list(points)[0]
        return winner

    def getScores(self):
        totalScores = {}
        for voter in self.voters:
            distances = {}
            minDis = float('inf')
            maxDis = 0


            for candidate in self.candidates:
                distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2 + (voter.z - candidate.z) ** 2)
                distances[candidate] = int(distance)
                if distance >= maxDis:
                    maxDis = int(distance)
                if distance <= minDis:
                    minDis = int(distance)
            disRange = maxDis - minDis
            scale = round(disRange/6)
            scoringMatrix = []
            zero = list(range(maxDis-scale,maxDis+1))
            one = list(range(maxDis-(scale*2),maxDis-scale))
            two = list(range(maxDis-(scale*3),maxDis-(scale*2)))
            three = list(range(maxDis-(scale*4),maxDis-(scale*3)))
            four = list(range(maxDis-(scale*5),maxDis-(scale*4)))
            five = list(range(minDis,maxDis-(scale*5)))
            scoringMatrix.append(zero)
            scoringMatrix.append(one)
            scoringMatrix.append(two)
            scoringMatrix.append(three)
            scoringMatrix.append(four)
            scoringMatrix.append(five)
            for candidate in self.candidates:
                dis = distances[candidate]
                i = 0
                for score in scoringMatrix:
                    if dis in score:
                        distances[candidate] = i
                        if candidate not in totalScores:
                            totalScores[candidate] = i
                        else:
                            totalScores[candidate] += i
                    i += 1
            voter.setScores(distances)
        return totalScores

    def runoff(self, can1,can2):
        can1tot = 0
        can2tot = 0
        for voter in self.voters:
            voterBallot = voter.scores
            score1 = voterBallot[can1]
            score2 = voterBallot[can2]
            if score1 > score2:
                can1tot += 1
            elif score2 > score1:
                can2tot += 1
        if can1tot == can2tot:
            return False
        elif can1tot > can2tot:
            return can1
        else:
            return can2

    def STAR(self):
        finalScores = self.getScores()
        sorted_dict = sorted(finalScores, key = finalScores.get, reverse=True)
        firstCandidate = sorted_dict[0]
        secondCandidate = sorted_dict[1]
        winner = self.runoff(firstCandidate, secondCandidate)
        return winner
    
    def distortion(self,candidate):
        if not candidate:
            return False
        
        sumDistance = 0 
        for voter in self.voters:
            distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2 + (voter.z - candidate.z)**2)
            sumDistance += distance

    
        distortion = sumDistance / self.minDistance
        return distortion
    
    def majorityCheck(self, candidate):
        if self.sorted_dict[0][1] > len(self.voters)/2:
            if candidate != self.sorted_dict[0][0]:
                return False
            else:
                return True
        return None

    def condorcetCheck(self, candidate):
        self.head_to_head()
        if self.hasCondorcetWinner:
            return candidate == self.condorcetWinner
        else:
            return None

def main():
    test = VoteResult3D(200, 15, "1D", "normal")
    print(test.pluralityVeto())
    print(test.condorcetCheck(test.plurality()))
    print(test.condorcetCheck(test.copeland()))
    
if __name__ == "__main__":  
    main()
    