import pygame

def reset(where, visited, image_and_caption):
     where = "bc"
     prov(where, visited, image_and_caption)
     for p in visited:
          visited[p] = 0

def visitedall(visited):
     for p in visited:
         if visited[p]==0: return False
     return True

def prov(where, visited, image_and_caption):
     current_image = pygame.image.load("images/"+where+ ".png")
     current_image = pygame.transform.scale(current_image, (400, 240))

     if where == "water":
         current_caption = "YOU FELL IN WATER! YOU LOSE!"
     elif where =="usa":
         current_caption = "YOU ENDED UP IN THE USA! YOU LOSE!"
     else:          
          visited[where]+=1          
          if visitedall(visited):
               current_image = pygame.image.load("canada.png")
               current_image = pygame.transform.scale(current_image, (400, 240))
               current_caption = "YOU WIN! YOU FOUND 'EM ALL!"
          else:               
               current_caption = "YOU ARE IN " + where.upper()
    
     image_and_caption["current_image"] = current_image
     image_and_caption["current_caption"] = current_caption
