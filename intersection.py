def subtract(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return (abs(x1 - x2), abs(y1 - y2))

def cross_product(p1, p2):
    x1, x2 = p1
    y1, y2 = p2
    return x1 * y2 - x2 * y1

def direction(p1, p2, p3):
    return cross_product(subtract(p3, p1), subtract(p2, p1))

# Checker om p3 ligger på linjen mellem p1 og p2
def on_segment(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return min(x1, x2) <= x3 <= max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2)

def intersect(p1, p2, p3, p4):
    direct1 = direction(p3, p4, p1)
    direct2 = direction(p3, p4, p2)
    direct3 = direction(p1, p2, p3)
    direct4 = direction(p1, p2, p4)

    if ((direct1 > 0 and direct2 < 0) or (direct1 < 0 and direct2 > 0)) and ((direct3 > 0 and direct4 < 0) or (direct3 < 0 and direct4 > 0)):
        return True

    elif direct1 == 0 and on_segment(p3, p4, p1):
        return True
    elif direct2 == 0 and on_segment(p3, p4, p2):
        return True
    elif direct3 == 0 and on_segment(p1, p2, p3):
        return True
    elif direct4 == 0 and on_segment(p1, p2, p4):
        return True
    else:
        return False

# Checker hvert linje segment i den nye linje, mod hvert linje segment i på skærmen for kollision
def other_collision(tempLst, permLst):
    collision_bool = False
    curr_tempLst = tempLst.head
    while curr_tempLst:
        curr_permLst = permLst.head
        while curr_permLst:
            if (intersect(curr_tempLst.data[0], curr_tempLst.data[1], curr_permLst.data[0], curr_permLst.data[1])):
                collision_bool = True
                break
            curr_permLst = curr_permLst.next
        curr_tempLst = curr_tempLst.next
    return collision_bool


def self_collision(tempLst):
    collision_bool = False
    curr_segment = tempLst.head
    while curr_segment:
        curr_tempLst2 = curr_segment.next
        while curr_tempLst2:
            if (curr_segment.next == curr_tempLst2 and curr_segment.data[0] == curr_tempLst2.data[1]):
                curr_tempLst2 = curr_tempLst2.next
                continue
            elif (intersect(curr_segment.data[0], curr_segment.data[1], curr_tempLst2.data[0], curr_tempLst2.data[1])):
                collision_bool = True
                break
            curr_tempLst2 = curr_tempLst2.next
        curr_segment = curr_segment.next
    return collision_bool

def collision(tempLst, permLst):
    return other_collision(tempLst, permLst) or self_collision(tempLst)
